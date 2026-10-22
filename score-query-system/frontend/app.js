// 原生前端：同源调用 Spring Boot 提供的 /api 接口（无需打包工具）
const API = '';               // 同源；若前后端分离部署可改为 'http://localhost:8080'
const SIZE = 10;
let studentPage = 0;

async function getJSON(url) {
    const res = await fetch(API + url);
    if (!res.ok) throw new Error('请求失败: ' + res.status);
    return res.json();
}

async function searchStudents() {
    const kw = document.getElementById('kw').value.trim();
    const data = await getJSON(`/api/students?keyword=${encodeURIComponent(kw)}&page=${studentPage}&size=${SIZE}`);
    const tbody = document.querySelector('#studentTable tbody');
    tbody.innerHTML = '';
    data.content.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${s.studentNo}</td><td>${s.name}</td><td>${s.className || '-'}</td><td>${s.major || '-'}</td>
            <td><button onclick="viewDetail(${s.id}, '${s.name}')">查看成绩</button></td>`;
        tbody.appendChild(tr);
    });
    document.getElementById('studentPageInfo').textContent =
        `第 ${data.number + 1} / ${data.totalPages} 页（共 ${data.totalElements} 条）`;
}

function prevStudentPage() { if (studentPage > 0) { studentPage--; searchStudents(); } }
function nextStudentPage() { studentPage++; searchStudents(); }

async function viewDetail(studentId, name) {
    document.getElementById('detailName').textContent = name;
    const [scores, gpa] = await Promise.all([
        getJSON(`/api/scores/student/${studentId}`),
        getJSON(`/api/stats/gpa?studentId=${studentId}`)
    ]);
    const tbody = document.querySelector('#scoreTable tbody');
    tbody.innerHTML = '';
    scores.forEach(v => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${v.courseName}</td><td>${v.courseCode}</td><td>${v.credit}</td>
            <td>${v.score}</td><td>${v.semester}</td><td>${v.examType}</td>`;
        tbody.appendChild(tr);
    });
    document.getElementById('gpaVal').textContent = gpa;
    document.getElementById('detailCard').style.display = 'block';
}

async function loadCourses() {
    const courses = await getJSON('/api/courses');
    const tbody = document.querySelector('#courseTable tbody');
    tbody.innerHTML = '';
    for (const c of courses) {
        let avg = '-';
        try { avg = await getJSON(`/api/stats/class-average?courseId=${c.id}`); } catch (e) {}
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${c.courseCode}</td><td>${c.courseName}</td><td>${c.credit}</td><td>${avg}</td>`;
        tbody.appendChild(tr);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    searchStudents();
    loadCourses();
});
