var log = console.log.bind(console)
var map = new AMap.Map("container", {
    resizeEnable: true,
    center: [118.159305, 24.715551],
    zoom: 13
});

AMap.event.addDomListener(document.getElementById('openDatabase'), 'click', function () {
    showAllHouse()
}, false);


// 实例化点标记
function addHouse(houseMap) {
    houseMap.forEach(function (value) {
        var marker = new AMap.Marker({
            icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
            position: [value[0].longitude, value[0].latitude]
        });
        marker.setMap(map);
        AMap.event.addListener(marker, 'click', function () {
            content = [];
            content.push("<div class=\"info-title\">丹厦房产</div><div class=\"info-content\">")
            value.forEach(function (item) {
                content.push("<p>地址：" + item.community);
                content.push("<p>" + item.houseaddress);
                content.push("<a  target='_blank' href=\""+item.detailurl+"\">详细信息</a>");
                content.push("<p>------------------------");
            })

            var infoWindow = new AMap.InfoWindow({
                isCustom: true,  //使用自定义窗体
                content: createInfoWindow(value[0], content.join("<br/>")),
                offset: new AMap.Pixel(16, -45),
                autoMove: true
            });
            infoWindow.open(map, marker.getPosition());
        });
    }, houseMap);

}


//实例化信息窗体
var title = '';
var content = [];


//构建自定义信息窗体
function createInfoWindow(house, content) {
    var info = document.createElement("div");
    info.className = "info";
    //可以通过下面的方式修改自定义窗体的宽高
    //info.style.width = "400px";
    // 定义顶部标题
    var top = document.createElement("div");
    var titleD = document.createElement("div");
    var closeX = document.createElement("img");
    top.className = "info-top";
    titleD.innerHTML = title;
    closeX.src = "https://webapi.amap.com/images/close2.gif";
    closeX.onclick = closeInfoWindow;
    top.appendChild(titleD);
    top.appendChild(closeX);
    info.appendChild(top);

    // 定义中部内容
    var middle = document.createElement("div");
    middle.className = "info-middle";
    middle.style.backgroundColor = 'white';
    middle.innerHTML = content;
    info.appendChild(middle);

    // 定义底部内容
    var bottom = document.createElement("div");
    bottom.className = "info-bottom";
    bottom.style.position = 'relative';
    bottom.style.top = '0px';
    bottom.style.margin = '0 auto';
    var sharp = document.createElement("img");
    sharp.src = "https://webapi.amap.com/images/sharp.png";
    bottom.appendChild(sharp);
    info.appendChild(bottom);
    return info;
}

//关闭信息窗体
function closeInfoWindow() {
    map.clearInfoWindow();
}




