var xmlHttp = createXMLHttpRequest();

function createXMLHttpRequest() {
    var xmlHttp;
    if (window.XMLHttpRequest) {
        xmlHttp = new XMLHttpRequest();
        if (xmlHttp.overrideMimeType)
            xmlHttp.overrideMimeType('text/xml');
    } else if (window.ActiveXObject) {
        try {
            xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {
            }
        }
    }
    return xmlHttp;
}

function showAllHouse() {
    var url = "/show";
    xmlHttp.open("GET", url, true);// 异步处理返回
    xmlHttp.onreadystatechange = processRequest;
    xmlHttp.setRequestHeader("Content-Type",
        "application/x-www-form-urlencoded;");
    xmlHttp.send();
}

function processRequest() {
    if (xmlHttp.readyState == 4) {
        if (xmlHttp.status == 200) {
            var request = JSON.parse(xmlHttp.responseText);
            log(request.length)
            var houseMap = new Map();
            for (var i = 0; i < request.length; i++) {
                log(request[i])
                var house = JSON.parse(request[i]);
                log(house["houseaddress"])
                var location = house.latitude+","+house.longitude
                if (houseMap.has(location)) {
                    houseMap.get(location).push(house)
                    log("has same location")
                    log(houseMap.size)
                }else{
                    log("setvalue")
                    var houselist = [house];
                    houseMap.set(location,houselist);
                    log(houseMap.size)
                }
            }
            log(houseMap.size)
            addHouse(houseMap)
        }
    }
}