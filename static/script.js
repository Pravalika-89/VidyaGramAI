async function predictCareer() {

    const maths = document.getElementById("maths").value;
    const programming = document.getElementById("programming").value;
    const communication = document.getElementById("communication").value;
    const problem_solving = document.getElementById("problem_solving").value;

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            maths: Number(maths),
            programming: Number(programming),
            communication: Number(communication),
            problem_solving: Number(problem_solving)
        })
    });

    const data = await response.json();

    document.getElementById("career").innerHTML = data.career;
    document.getElementById("roadmap").innerHTML =
        data.roadmap.map(item => `<li>${item}</li>`).join("");
}