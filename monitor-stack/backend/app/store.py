"""告警存储（内存）。

演示用内存实现；生产替换为 Redis / 数据库以保证多实例一致与持久化。
"""
import time
import uuid
from dataclasses import dataclass, field


@dataclass
class Alert:
    id: str
    fingerprint: str
    status: str               # firing / resolved
    labels: dict
    annotations: dict
    acked: bool = False
    received_at: float = 0.0


class AlertStore:
    def __init__(self):
        self.alerts: list[Alert] = []

    def add_from_webhook(self, payload: dict) -> list[Alert]:
        created = []
        for a in payload.get("alerts", []) or []:
            alert = Alert(
                id=str(uuid.uuid4()),
                fingerprint=a.get("fingerprint", str(uuid.uuid4())),
                status=a.get("status", payload.get("status", "firing")),
                labels=a.get("labels", {}) or {},
                annotations=a.get("annotations", {}) or {},
                received_at=time.time(),
            )
            self.alerts.append(alert)
            created.append(alert)
        # 仅保留最近 500 条，避免内存无限增长
        if len(self.alerts) > 500:
            self.alerts = self.alerts[-500:]
        return created

    def list(self) -> list[dict]:
        items = sorted(self.alerts, key=lambda x: x.received_at, reverse=True)
        return [self._to_dict(a) for a in items]

    def ack(self, alert_id: str) -> bool:
        for a in self.alerts:
            if a.id == alert_id:
                a.acked = True
                return True
        return False

    @staticmethod
    def _to_dict(a: Alert) -> dict:
        return {
            "id": a.id,
            "fingerprint": a.fingerprint,
            "status": a.status,
            "labels": a.labels,
            "annotations": a.annotations,
            "acked": a.acked,
            "received_at": a.received_at,
        }


store = AlertStore()
