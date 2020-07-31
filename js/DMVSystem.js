//列表的数据源和可视化
var nav = document.getElementById('nav').getElementsByTagName('li');
var part = document.getElementsByClassName('part');


var pageIntroduct = document.getElementById('page-introduct');

//表示状态
var state = false;

var searchPart = document.getElementById('searchPart');

//让对应区域消失
for(var m = 1; m < nav.length; m++){
    nav[m].className = 'iconfont';
    part[m].style.display= "none";
}


//读取文件
var file1 = document.getElementById('file1');


    var data = "";

    file1.onchange = function(){

        var file = file1.files[0];

        var reader = new FileReader();

        reader.readAsText(file,'utf-8');

        reader.onload = function(){

            data = reader.result;

        }
        
    }

//找类名
function findClass(dataSet, pos) {

    var res = new Array();

    for(var i = 1; i < dataSet.length; i++){

        if(!res.includes(dataSet[i][pos])) 
            res.push(dataSet[i][pos]);

    }

    return res;

}
        

//创建平行坐标系
function createParallelAxis(dataSet){

    var columns_length = dataSet[0].length;
    var parallelAxis = new Array();
    var featName = dataSet[0].slice(1, columns_length - 1);
    for(var i = 0; i < featName.length; i++){
        
        parallelAxis.push({dim: i,name:featName[i]});
    }

    return parallelAxis;
}   


//随机生成颜色
function IsColor(arr,classes){
    var len = arr.length;
    var colors = [
        "#6C6C6C", "#AE0000", "#f079b4","#f00bf0", "#8600FF",
        "#2828FF", "#0072E3", "#00CACA", "#02DF82", "#00DB00", 
        "#82D900", "#e0e008", "#C6A300", "#f17f0d", "#D94600", 
        "#a05959", "#949449",  "#4F9D9D", "#5ba3a3", "#9F4D95"
    ];

    var basic = Math.floor(Math.random()*colors.length);

    var color = colors[(basic + classes.indexOf(arr[len - 1])) % 20];

    return color;
}


//创平行坐标系系列
function createParallelSeries(dataSet, classes){

    

    var rows_length = dataSet.length, 
        columns_length = dataSet[0].length;

    var len = classes.length;

    var feature = {};

    var series = new Array();

    for(var i = 0; i < len; i++){
        feature[classes[i]] = new Array();
    }

    for(var i = 1; i < rows_length - 1; i++){
        var temp = dataSet[i].slice(1, columns_length - 1);
        feature[dataSet[i][columns_length - 1]].push(temp);
    }

    for(var i = 0; i < len; i++){
        series.push({
            name: classes[i],
            type: 'parallel',
            data: feature[classes[i]]
        });
    }

    return series;
}


//创平行坐标系option
function ParallelOption(classes,parallelAxis,series){
    var option = {
        title: {
            text:'平行坐标系',
            left:'center'
        },
        legend: {
            bottom: 30,
            data: classes,
            itemGap: 20,
            textStyle: {
                fontSize: 14
            }
        },
        tooltip: {
            padding: 10,
            backgroundColor: '#222',
            borderColor: '#777',
            borderWidth: 1,
        },
        parallelAxis: parallelAxis,
        parallel: {
            left: '5%',
            right: '18%',
            bottom: 100,
            parallelAxisDefault: {
                type: 'value',
                splitLine: {
                    show: false
                }
            }
        },
        series: series
    };
    return option;
}


//RadViz雷达图
function radViz(dataSet, R, classes) {

    var columns_Count = dataSet[0].length, rows_Count = dataSet.length;;

    var theta = 360.0 / (columns_Count - 2);

    dataSet = normalization(dataSet);

    var res = {
        features:[]
    };

    for(var i in classes) {

        res[classes[i]] = new Array();

    }

    for(var rad = 0.0, i = 1;i < columns_Count -1;++i, rad += theta) {

        x = R * Math.cos(rad/180*Math.PI);

        y = R * Math.sin(rad/180*Math.PI);

        res.features.push([x, y])

    }


    for(var j = 1;j < rows_Count;++j) {

        var x = 0.0, y = 0.0;

        for(var rad = 0.0, i = 1;i < columns_Count -1;++i, rad += theta) {

            x += R * dataSet[j][i] * Math.cos(rad / 180.0 * Math.PI);

            y += R * dataSet[j][i] * Math.sin(rad / 180.0 * Math.PI);

        }

        res[dataSet[j][columns_Count - 1]].push([x, y]);

    }

    return res;

}

//求出RadViz雷达图坐标
var normalization = function(dataSet) {

    var columns_Count = dataSet[0].length, 
        rows_Count = dataSet.length;

    for(var i = 1;i < columns_Count - 1;++i) {

        var maxi = -0x3f3f3f3f, mini = 0x3f3f3f3f;

        for(var j = 1;j < rows_Count;++j) {

            maxi = Math.max(dataSet[j][i], maxi)

            mini = Math.min(dataSet[j][i], mini)

        }

        for(var j = 1;j < rows_Count;++j) {

            dataSet[j][i] -= mini;

            dataSet[j][i] /= (maxi - mini);

        }

    }

    return dataSet;

}

//创建雷达图option
function creatRadVizOption(series,classes){
    var option = {
        title:{
            text:'RadViz雷达图',
            left:'center'
        },
       legend: {
            bottom: 0,
            data: classes
       },
       tooltip:{
            formatter: function (params) {
                    return params.seriesName + ' :<br/>'
                    + params.value[0] + '<br/>'
                    + params.value[1];
            },
       },
       xAxis:{},
       yAxis:{},
       series:series
   }
   return option;
}

//创建RadViz系列
function RadVizSeries(classes,sum){
    var len = classes.length;
    var series = [];
    for(var i = 0; i < len; i++){
        series.push({
            name: classes[i],
            type:'scatter',
            data:sum[classes[i]]
        })
    }
    return series;
}


//求出Andrew坐标
function Andrews(data, l, h, accuracy){

    var columns_Count = data.length;

    var args = new Array(), 
        res = new Array();

    for(var i = 1; i < columns_Count - 1;i++) {

        args.push(parseFloat(data[i]));

    }

    for(var x = l;x <= h;x += accuracy) {

        var y = 0;

        for(var i = 0; i < args.length; i++) {

            if(i == 0) {

                y += args[i]/Math.sqrt(2);

            }else if(i % 2) {

                y += args[i]*Math.cos((i - 1)/2*x);

            } else {

                y += args[i]*Math.sin(i/2*x);

            }
        }

        res.push([x, y]);

    }

    return res;
}

//生成Andrew的option
function AndrewOption(classes,series){
    var option = {
        title:{
            text:'傅里叶图',
            left:'center'
        },
       legend: {
            bottom: 0,
            data: classes
       },
       tooltip:{
            formatter: function (params) {
                    return params.seriesName + ' :<br/>'
                    + params.value[0] + '<br/>'
                    + params.value[1];
            },
       },
       xAxis:{},
       yAxis:{},
       series:  series
  
   }
   return option;
}

//生成Andrew的series
function ASeries(dataSet, classes) {

    var colors = [
        "#6C6C6C", "#AE0000", "#f079b4","#f00bf0", "#8600FF",
        "#2828FF", "#0072E3", "#00CACA", "#02DF82", "#00DB00", 
        "#82D900", "#e0e008", "#C6A300", "#f17f0d", "#D94600", 
        "#a05959", "#949449",  "#4F9D9D", "#5ba3a3", "#9F4D95"
    ];

    var series = [];

    var len = dataSet[0].length;

    var basic = Math.floor(Math.random()*colors.length);

    for(var i = 1; i < dataSet.length; i++){

            var item = {
                name: dataSet[i][len - 1],

                type: 'line',

                data: Andrews(dataSet[i], -Math.PI, Math.PI, 0.1)
            };

        series.push(item);
    }
    return series;
}


//找每个数的百分比
function CalPercent(dataSet,classes){
    var lines = dataSet.length;
    var len = dataSet[0].length;
    var arr = [];
    for(var j = 0;j < classes.length; j++){
        var x = 0;
        for(var i = 1; i < lines; i++){
            if(dataSet[i][len - 1] == classes[j]){
                x++;
            }
        }
        arr.push(x);
    }
    return arr;
}

//条形图option
function BarOption(arr,classes){
    var option = {
        title:{
            text:'条形图',
            left:'center'
        },
        tooltip: {
          
        },
        xAxis:{
            type:'category',
            data: classes
        },
        yAxis:{
            type:'value'
        },
        series:[{
            data: arr,
            type:'bar',
            itemStyle:{
                color: '#a770f0'
            }
        }]
    
    }
    return option;
}

//生成饼图数据
function CreateParData(arr,res){
    var data = [];
    for(var i = 0; i < res.length; i++){
        var obj = new Object();
        obj.name = res[i];
        obj.value = arr[i];
        data.push(obj); 
    }
    return data;
}

//生成饼图option
function ParOption(data){
    var option = {
        title:{
            text:'饼状图',
            left:'center'
        },
        legend: {
            bottom: 0,
        },
        tooltip: {
        
        },
        series:[{
            data: data,
            type:'pie',
        }]

    }
    return option;
}

var process = document.getElementById('process').getElementsByTagName('li');

process[0].onclick = function() {

    alert("pretreat");

};

process[1].onclick = function() {

    alert("fit");

};

process[2].onclick = function() {

    alert("predict");

};

var chartList = document.getElementById('chartList').getElementsByTagName('li');


//每个数据源的导入
var source = document.getElementById('source').getElementsByTagName('span');

for(var i = 0; i < source.length; i++){
    source[i].index = i;
    source[i].onclick = function(){
        state = true;

        source[this.index].innerHTML = "已导入";

        source[this.index].style.color = '#75DAAD';

        source[this.index].style.backgroundColor = 'rgba(117, 218, 173,0.2)';
        
        for(var i = 0; i < source.length; i++){
            source[i].onclick = null;
        }

        var submitdata = {

            dataSet: data,

            sep: ","

        };

        //发送请求
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST","http://120.76.139.47:8000/api-DataFrame",true);

        xmlhttp.setRequestHeader("Content-type","application/json");

        xmlhttp.send(JSON.stringify(submitdata));

        xmlhttp.onreadystatechange = function() {

            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                
                dataSet = eval(xmlhttp.responseText);

                createTable(dataSet);

                var rows_length = dataSet.length, 
                    columns_length = dataSet[0].length;

                for(var i = 0; i < chartList.length; i++){
                    chartList[i].index = i;
                    chartList[i].onclick = function(){
                        clearName(chartList);
                        chartList[this.index].className = 'active';
                        var classes = findClass(dataSet,columns_length - 1);
                        // document.getElementById('chartShow').innerHTML = '';
                       if(this.index == 2){
                            // var classes = findClass(dataSet,columns_length - 1);

                            var arr = CalPercent(dataSet,classes);

                            var option = BarOption(arr,classes);
                        } else if(this.index == 3){
                            // var classes = findClass(dataSet,columns_length - 1);

                            var arr = CalPercent(dataSet,classes);

                            var data = CreateParData(arr, classes);

                            var option = ParOption(data);
                        } else if(this.index == 4){
                            //平行坐标
                            // var classes = findClass(dataSet, columns_length - 1);
                                            
                            var parallelAxis = createParallelAxis(dataSet);

                            var series = createParallelSeries(dataSet, classes);

                            var option = ParallelOption(classes,parallelAxis,series);
                       
                        } else if(this.index == 5){
                            // var classes = findClass(dataSet,dataSet[0].length - 1);

                            var sum = radViz(dataSet, 1, classes);

                            var series = RadVizSeries(classes, sum);
                          
                            for(var fe in sum.features) {

                                series.push({
                                           name: dataSet[0][parseInt(fe) + 1],
                                           type:'scatter',
                                           data: [sum.features[parseInt(fe)]]        
                                       });
                                classes.push(dataSet[0][parseInt(fe) + 1]);
                            }
                            var option = creatRadVizOption(series,classes);

                       } else if(this.index == 6){
                            
                            // var classes = findClass(dataSet, dataSet[0].length - 1);
                            if(classes > 20) return;
                            var series = ASeries(dataSet, classes);
                            var option = AndrewOption(classes,series);
                       } else {
                           var option = {};
                       }
                           
                        var myChart = echarts.init(document.getElementById('chartShow'),'light');
                        
                        myChart.setOption(option,true);

                        
                    }
                }

            }
        }
    
    }
}

//标签切换
function tabChange(){
    if(state == true){
        for(var j = 0; j < nav.length; j++){
            nav[j].className = 'iconfont';
            part[j].style.display = 'none';
        }
        if(this.index == 0){
            pageIntroduct.innerHTML = '数据源';
            searchPart.style.display = 'block';
        } else if(this.index == nav.length - 1){
            pageIntroduct.innerHTML = '可视化';
            searchPart.style.display = 'none';
        }
        this.className = 'active' + ' ' + 'iconfont';
        part[this.index].style.display = 'block';
    } else {
        alert('请导入数据源');
    }
}


//标签页
for(var i = 0; i < nav.length; i++){
    nav[i].index = i;
    nav[i].onclick = tabChange;
}



  

//清除class
function clearName(arr){
    for(var i = 0,len = arr.length; i < len; i++){
        arr[i].className = "";
    }
}

//生成表格
var createTable = function(array) {

    var table = '<table>', 
        allRows = array;

    for(var singleRow = 0; singleRow < allRows.length;singleRow++) {

        if(singleRow === 0) {

            table += '<table>';

            table += '<tr>';

        } else {

            table += '<tr>';
        }

        var rowCells = allRows[singleRow];

        for(var rowCell = 0;rowCell < rowCells.length; rowCell++) {

            if(singleRow === 0){

                table += '<th>';

                table += rowCells[rowCell];

                table += '</th>';

            } else {

                table += '<td>';

                table += rowCells[rowCell];

                table += '</td>';

            }
        }
        if (singleRow === 0) {

            table += '</tr>';

            table += '</thead>';

            table += '<tbody>';

        } else {

            table += '</tr>';
        }
    }

    table += '</tbody>';

    table += '</table>';
    
    document.getElementById('tableShow').innerHTML = table;

}
