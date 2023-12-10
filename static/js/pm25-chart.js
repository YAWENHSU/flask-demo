
const chart1 = echarts.init(document.getElementById('main'));
const chart2 = echarts.init(document.getElementById('six_counties'));
const chart3 = echarts.init(document.getElementById('county'));
const selectCountyEl = document.querySelector("#selectCounty");

selectCountyEl.addEventListener("change", () => {
    console.log(selectCountyEl.value);
    drawCountyPM25(selectCountyEl.value);
});

window.onresize = function () {
    chart1.resize();
    chart2.resize();
    chart3.resize();
};


//繪製圖形
drawPM25();


//共用繪製函式
function chartPic(chart, title, label, xData, yData, color = "#00008b") {
    let option = {
        title: {
            text: title
        },
        tooltip: {},
        legend: {
            data: [label]
        },
        xAxis: {
            data: xData
        },
        yAxis: {},
        series: [
            {
                itemStyle: { color: color },
                name: label,
                type: 'bar',
                data: yData
            }
        ]
    };

    chart.setOption(option);

}

function drawCountyPM25(county) {
    //ajax
    chart3.showLoading();
    $.ajax(
        {
            url: "/county-pm25-json/" + county,
            type: "GET",
            dataType: "json",
            success: (result) => {
                chart3.hideLoading();
                if (!result["success"]) { county = county + " 輸入不正確..."; }
                console.log(result);
                chartPic(chart3, county, "PM2.5",
                    Object.keys(result['pm25']),
                    Object.values(result['pm25']),)

            },
            error: () => {
                chart3.hideLoading();
                alert("取得資料失敗!");
            }
        }
    )
}


// function echartSixPm25(result) {
//     let option = {
//         title: {
//             text: '六都PM2.5平均值'
//         },
//         tooltip: {},
//         legend: {
//             data: ['PM2.5']
//         },
//         xAxis: {
//             data: Object.keys(result)
//         },
//         yAxis: {},
//         series: [
//             {
//                 itemStyle: { color: '#8b008b' },
//                 name: 'PM2.5',
//                 type: 'bar',
//                 data: Object.values(result)
//             }
//         ]
//     };

//     myChart2.setOption(option);

// }

// function echartPic1(result) {
//     let option = {
//         title: {
//             text: result['title']
//         },
//         tooltip: {},
//         legend: {
//             data: ['PM2.5']
//         },
//         xAxis: {
//             data: result['xData']
//         },
//         yAxis: {},
//         series: [
//             {
//                 name: 'PM2.5',
//                 type: 'bar',
//                 data: result['yData']
//             }
//         ]
//     };

//     myChart.setOption(option);
// }

function drawPM25() {
    //ajax
    chart1.showLoading();
    chart2.showLoading();
    $.ajax(
        {
            url: "/pm25-json",
            type: "GET",
            dataType: "json",
            success: (result) => {
                chart1.hideLoading();
                chart2.hideLoading();
                console.log(result);
                chartPic(chart1, result['title'], "PM2.5",
                    (result['xData']),
                    (result['yData']));

                chartPic(chart2, "六都PM2.5平均值", "PM2.5",
                    Object.keys(result["sixData"]),
                    Object.values(result["sixData"]), "#ff69b4");

                drawCountyPM25(result["county"]);

                //echartSixPm25(result["sixData"]);
            },
            error: () => {
                chart1.hideLoading();
                chart2.hideLoading();
                alert("取得資料失敗!");
            }
        }
    )
}