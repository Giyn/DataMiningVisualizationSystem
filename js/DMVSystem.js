//列表的数据源和可视化
var nav = document.getElementById('nav').getElementsByTagName('li');
//对应区域
var part = document.getElementsByClassName('part');

//对应的页面名字
var pageIntroduct = document.getElementById('page-introduct');

//表示状态，有无导入数据源
var state = false;


//服务器地址
var serverAddress = "http://127.0.0.1:4000";


 //获取显示加载图片
 var LoadingPic = document.getElementById('LoadingPic');


//搜索区域
var searchPart = document.getElementById('searchPart');

//让对应区域消失
for(var m = 1; m < nav.length; m++){
    nav[m].className = 'iconfont';
    part[m].style.display= "none";
}



//读取文件
var file1 = document.getElementById('file1');



var data = "";



//根据这个来请求
var num;

// var file = document.getElementById('source').getElementsByTagName('input');



// file1.onchange = function(){

//     var file = file1.files[0];

//     var filename = file.name;


//     if(filename == 'iris.csv'){
//         num = 1;
//     } else if(filename == 'tree.csv'){
//         num = 2;
//     } else if(filename == 'cancer.csv'){
//         num = 3;
//     } else if(filename == 'housing.csv'){
//         num = 4;
//     } else if(filename == 'forestfires.csv'){
//         num = 5;
//     } else if(filename == 'spam_ham_dataset.csv'){
//         num = 6;
//     } else {
//         num = 0;
//     }

//     document.getElementById('fileName').innerHTML = filename;

//     var reader = new FileReader();


//     reader.readAsText(file,'utf-8');

//     reader.onload = function(){

//         data = reader.result;

//     }
    
// }


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
        "#5B8FF9", "#5AD8A6", "#5D7092","#F6BD16", "#E8684A",
        "#6DC8EC", "#9270CA", "#FF9D4D", "#FF9D4D", "#FF99C3", 
    ];

    var basic = Math.floor(Math.random()*colors.length);

    var color = colors[(basic + classes.indexOf(arr[len - 1])) % 10];

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
            // itemStyle: {
            //     color: IsColor(dataSet[i], classes)
            // },
            data: feature[classes[i]]
        });
    }

    return series;
}


//创平行坐标系option
function ParallelOption(classes,parallelAxis,series){
    var option = {
        title: {
            text:'平行坐标图',
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
            text:'Andrew图',
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

    // var colors = [
    //     "#5B8FF9", "#5AD8A6", "#5D7092","#F6BD16", "#E8684A",
    //     "#6DC8EC", "#9270CA", "#FF9D4D", "#FF9D4D", "#FF99C3", 
    // ];
    //     "#82D900", "#e0e008", "#C6A300", "#f17f0d", "#D94600", 
    //     "#a05959", "#949449",  "#4F9D9D", "#5ba3a3", "#9F4D95"
    var series = [];

    var len = dataSet[0].length;

    // var basic = Math.floor(Math.random()*colors.length);

    for(var i = 1; i < dataSet.length; i++){

            var item = {
                name: dataSet[i][len - 1],

                type: 'line',

                data: Andrews(dataSet[i], -Math.PI, Math.PI, 0.1),

                // itemStyle: {
                    
                //     color:function(params){

                //         var colors = [
                //             "#5B8FF9", "#5AD8A6", "#5D7092","#F6BD16", "#E8684A",
                //             "#6DC8EC", "#9270CA", "#FF9D4D", "#FF9D4D", "#FF99C3", 
                //         ];
                //         return colors[params.dataIndex];

                //     }
                //     // color: colors[(basic + classes.indexOf(dataSet[i][len - 1])) % 10]
                // }
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
            type:'bar'
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

//随机两列散点
function RandomScatter(dataSet, classes){
    var len = dataSet[0].length;
    var x = Math.floor(Math.random()*(len - 2) + 1);
    var y = Math.floor(Math.random()*(len - 2) + 1);
    var obj = {};
    obj.x = dataSet[0][x];
    obj.y = dataSet[0][y];

    
        for(var i = 0; i < classes.length; i++){
            obj[classes[i]] = [];
            for(var j = 1; j < dataSet.length; j++){
            if(classes[i] == dataSet[j][len - 1]){
                var arr = [];
                arr.push(dataSet[j][x]);
                arr.push(dataSet[j][y]);
                obj[classes[i]].push(arr);
            }
        }
    }
    return obj;
}

//散点系列
function ScatterSeries(dataSet,classes,obj){
    var series = [];
    for(var i = 0; i < classes.length; i++){
        series.push({
            name:classes[i],
            type:'scatter',
            data: obj[classes[i]]
        })
    }
    return series;
}

//散点Option
function ScatterOption(series,classes,obj){
    var option = {
            title:{
                text:'散点图',
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
            xAxis:{
                name: obj.x
            },
            yAxis:{
                name: obj.y
            },
            series: series
    }
    return option;
}

//折线系列
function LineSeries(classes,obj){
    var series = [];
    for(var i = 0; i < classes.length; i++){
        series.push({
            name: classes[i],
            type: 'line',
            smooth: false,
            data: obj[classes[i]]
        });
    }
    return series;

}

//折线图Option
function LineOption(series,classes,obj){
    var option = {
        title:{
            text:'折线图',
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
        xAxis: {
            name: obj.x,
        },
        yAxis: {
            name: obj.y,
        },
        series: series
    };
    return option;
}






//从后端拿对应的数据源
var source = document.getElementById('source').getElementsByTagName('span');

var filename = document.getElementById('source').getElementsByTagName('h3');

//数据集简介
var fileIntroduct = document.getElementById('source').getElementsByTagName('p');



for(var i = 0; i < source.length; i++){
    source[i].index = i;
    source[i].onclick = function(){


        state = true;

        num = this.index;

        var submitdata = this.index;

        for(var i = 0; i < source.length; i++) {

            source[i].innerHTML = "导入数据集";

            source[i].style.backgroundColor = '#F9D56E';

            source[i].style.color = '#000000';


        }

        //显示加载
        LoadingPic.style.display = 'block';
        
        source[this.index].innerHTML = "正在导入";

        source[this.index].style.color = '#75DAAD';

        source[this.index].style.backgroundColor = 'rgba(218, 117, 173,0.2)';

        var index = source[this.index];

        document.getElementById('fileName').innerHTML = filename[this.index].innerHTML;

        document.getElementById('fileSay').innerHTML = fileIntroduct[this.index].innerHTML;

        //发送请求
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST",serverAddress + "/api-getDataSet",true);

        xmlhttp.setRequestHeader("Content-type","application/json");

        xmlhttp.send(JSON.stringify(submitdata));

        xmlhttp.onreadystatechange = function() {

            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                
                dataSet = eval(xmlhttp.responseText);

                dataSet_string = xmlhttp.responseText;

                fit_target = dataSet[0][dataSet[0].length - 1];

                for(var j = 0;j < funcList.length;++j) {

                    funcList[j].className = '';

                }
                
                funcList[num].className = 'active';
        
                fit_model = num + 1;

                createTable(dataSet);

                state = true;
        
                index.innerHTML = "已导入";
        
                index.style.color = '#75DAAD';
        
                index.style.backgroundColor = 'rgba(117, 218, 173,0.2)';

                //隐藏图片
                LoadingPic.style.display = 'none';

                alert("数据加载完毕，前往‘可视化’查看");

            }
        }
    }
}




//获取图表选择
var chartList = document.getElementById('chartList').getElementsByTagName('li');


//可视化图表
for(var i = 0; i < chartList.length; i++){
    chartList[i].index = i;
    chartList[i].onclick = function(){
        var rows_length = dataSet.length, 
            columns_length = dataSet[0].length;
        clearName(chartList);
        chartList[this.index].className = 'active';
        var classes = findClass(dataSet,columns_length - 1);
        // document.getElementById('chartShow').innerHTML = '';
        if(classes.length > 6){
            for(var j = 0; j < rows_length; j++){
                
                dataSet[j].push('one');
                
            }
            classes = ['one'];
        }

        if(this.index == 0){
            //散点
            var obj = RandomScatter(dataSet,classes);
            
            var series = ScatterSeries(dataSet,classes,obj);
            
            var option = ScatterOption(series,classes,obj);
        } else if(this.index == 1){
            //折线
            var obj = RandomScatter(dataSet,classes);
            for(var i = 0; i < classes.length; i++){
                
                var name = classes[i];
                // console.log(obj[name]);
                obj[name].sort(function(a, b){
                    var value1 = a[0];
                    var value2 = b[0];
                    return value1 - value2;
                });
            }
            var series = LineSeries(classes,obj);
            var option = LineOption(series,classes,obj);

        } else if(this.index == 2){
            //条形

            var arr = CalPercent(dataSet,classes);

            var option = BarOption(arr,classes);
        } else if(this.index == 3){
            //饼状

            var arr = CalPercent(dataSet,classes);

            var data = CreateParData(arr, classes);

            var option = ParOption(data);
        } else if(this.index == 4){
            //平行坐标
                            
            var parallelAxis = createParallelAxis(dataSet);

            var series = createParallelSeries(dataSet, classes);

            var option = ParallelOption(classes,parallelAxis,series);
        
        } else if(this.index == 5){
            //雷达图

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
            //傅里叶 
            
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

// 生成表格
function createTable(array) {

    var table = '<table>', 
        allRows = array;

    for(var singleRow = 0; singleRow < allRows.length;singleRow++) {

        if(singleRow === 0) {

            table += '<thead>';

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



// function createTable(array) {

//     var table = '<table>', 
//         allRows = array;

//         table += '<thead>';
//             table += '<tr>';
//     for(var i = 0; i < allRows[0].length; i++){
//         table += '<th>';
//         if(i = 0){
//             table += '</th>';
//         } else {

//             table += `<input type='checkbox' name='' class='choose'></th>`;
//         }
//     }

//     for(var singleRow = 0; singleRow < allRows.length; singleRow++){
//         if(singleRow == 0){
//             table += '<tbody>';
//                 table += '<tr>';
//         } else {
//             table += '<tr>';
//         }

//         var rowCells = allRows[singleRow];

//         for(var rowCell = 0; rowCell < rowCells.length;rowCell++){
//             table += '<td>';
//                 table += rowCells[rowCell];
//                 table += '</td>';
//         }
//         table += '</tr>';
//     }
//     table += '</tbody>';
//     table += '</table>';
//     document.getElementById('tableShow').innerHTML = table;
// }




//数据集和模型相关
var dataSet = null;

var dataSet_string = "";

var data_hashKey = "";

var model_hashKey = "";

var fit_model = 5;

var fit_target = "";

var process = document.getElementById('process').getElementsByTagName('li');


//点击提交并预处理
process[0].onclick = function() {

    //显示加载
    LoadingPic.style.display = 'block';

    var submitdata = {

        dataSet: dataSet_string,

        dropColumns: [] ,

        discreteColumns: [],

        textColumn: "text"

    };
    
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("POST",serverAddress + "/api-pretreatment",true);

    xmlhttp.setRequestHeader("Content-type", "application/json");

    xmlhttp.send(JSON.stringify(submitdata));

    xmlhttp.onreadystatechange = function() {

        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {

            data_hashKey = xmlhttp.responseText;

            console.log(data_hashKey);

        } 
         //加载隐藏
         LoadingPic.style.display = 'none';
    }

};

//点击训练
process[1].onclick = function() {

    if(data_hashKey == "") {

        alert("数据尚未进行预处理");

        return;

    }

    //显示加载
    LoadingPic.style.display = 'block';

    var submitdata = {

        hashKey: data_hashKey,

        model: fit_model,

        target: fit_target

    };
    
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("POST", serverAddress + "/api-fit",true);

    xmlhttp.setRequestHeader("Content-type", "application/json");

    xmlhttp.send(JSON.stringify(submitdata));

    xmlhttp.onreadystatechange = function() {

        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {

            var data = JSON.parse(xmlhttp.responseText);

            CreatImg(data.images);

            model_hashKey = data["hashKey"];

            var str = '模型评估参数：' + data.cv_score;

            document.getElementById('assess').innerHTML = str;

        } 
         //加载隐藏
         LoadingPic.style.display = 'none';
    }

};

//生成并插入图片
function CreatImg(arr){
    var image = '';
    for(var i = 0; i < arr.length; i++){
        var str = arr[i];
        var dom = '<img src= data:image/png;base64,'+str.substring(2,str.length - 1)+'>';
        image += dom;
    }
    document.getElementById('chartResult').innerHTML = image;
}

//点击预测
process[2].onclick = function() {

    alert("FREE版还不能进行预测，请尝试我们的PRO版。^_^")

    return

    var submitdata = {

        hashKeyI: data_hashKey,

        hashKeyII: model_hashKey

    };
    
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("POST",serverAddress + "/api-predict",true);

    xmlhttp.setRequestHeader("Content-type", "application/json");

    xmlhttp.send(JSON.stringify(submitdata));

    xmlhttp.onreadystatechange = function() {

        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {

            var temp = eval(xmlhttp.responseText);

            createTable(temp);

            console.log(temp);

        }
    }

};

//算法选择
var funcList = document.getElementById('funcList').getElementsByTagName('li');

for(var i = 0;i < funcList.length;++i) {

    funcList[i].index = i;

    funcList[i].onclick = function() {

        alert("FREE版还不能选择算法，请尝试我们的PRO版。^_^")

    };


}