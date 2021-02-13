var btnSubmit = document.querySelector("#submit");
var text = document.querySelector("#text-input");
var resultDiv = document.querySelector("#result");
var btnDelete = document.querySelector("#delete");
var divChart = document.querySelector("#chart");

function drawChart(title, datas) {
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Tiêu cực', 'Trung tính', 'Tích cực'],
            datasets: [{
                label: '# of Votes',
                data: datas,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: title
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

btnSubmit.addEventListener('click', async e => {
    e.preventDefault()

    if (text.value === '') { return; }

    const res = await fetch('/api/predict', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text.value })
    })

    const { title, probabilities } = await res.json();
    // var str = JSON.stringify(probabilities);
    // resultDiv.innerHTML = str;
    var datas = Object.values(probabilities);
    drawChart(text.value, datas);
});

btnDelete.addEventListener('click', () => {
    divChart.innerHTML = '';
    text.value = "";
})