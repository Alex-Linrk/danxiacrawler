var log = console.log.bind(console)
var marker, map = new AMap.Map("container", {
    resizeEnable: true,
    center: [118.159305, 24.715551],
    zoom: 13
});
AMap.event.addDomListener(document.getElementById('addMarker'), 'click', function () {
    addMarker();
}, false);
AMap.event.addDomListener(document.getElementById('updateMarker'), 'click', function () {
    marker && updateMarker();
}, false);
AMap.event.addDomListener(document.getElementById('clearMarker'), 'click', function () {
    if (marker) {
        marker.setMap(null);
        marker = null;
    }
}, false);
AMap.event.addDomListener(document.getElementById('openDatabase'), 'click', function () {
    showAllHouse()
}, false);


function updateMarker() {
    // 自定义点标记内容
    var markerContent = document.createElement("div");

    // 点标记中的图标
    var markerImg = document.createElement("img");
    markerImg.className = "markerlnglat";
    markerImg.src = "http://webapi.amap.com/theme/v1.3/markers/n/mark_r.png";
    markerContent.appendChild(markerImg);

    // 点标记中的文本
    var markerSpan = document.createElement("span");
    markerSpan.className = 'marker';
    markerSpan.innerHTML = "Hi，我换新装备啦！";
    markerContent.appendChild(markerSpan);

    marker.setContent(markerContent); //更新点标记内容
    marker.setPosition([116.391467, 39.927761]); //更新点标记位置
}

// 实例化点标记
function addMarker() {
    marker = new AMap.Marker({
        icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
        position: [118.137347, 24.715551]
    });
    marker.setMap(map);
}

// 实例化点标记
function addHouse(houseMap) {
    var keys = houseMap.keys()
    houseMap.forEach(function (value, key) {
        var marker = new AMap.Marker({
            icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
            position: [value[0].longitude, value[0].latitude]
        });
        marker.setMap(map);
        AMap.event.addListener(marker, 'click', function () {
            content = [];
            value.forEach(function (item) {
                    log(item.houseaddress)
                    content.push("<img src='https://webapi.amap.com/images/sharp.png'>地址：" + item.community);
                    content.push("电话：010-64733333");
                    content.push("<a href='" + item.detailurl + "'>详细信息</a>");
            })

            var infoWindow = new AMap.InfoWindow({
                isCustom: true,  //使用自定义窗体
                content: createInfoWindow(value[0], content.join("<br/>")),
                offset: new AMap.Pixel(16, -45)
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
    closeX.src = house.detailurl;
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




