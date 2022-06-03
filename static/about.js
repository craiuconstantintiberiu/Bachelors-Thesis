var canvas = document.getElementById('Canvas');
var context = canvas.getContext("2d");

pointMap = new Map();


// Map sprite
var mapSprite = new Image();
mapSprite.src = "../static/SeeroseSample.JPG";
points=["Left Acetabular", "Left Femoral Head", "Right Femoral Head", "Right Acetabular"]

var unsetPoints = function () {
    console.log("Map keys")
    for (t in pointMap.keys()){
        console.log(t)
    }
    let pointsUnused = [];
    for (var i = 0; i<points.length; i++) {
        console.log(points[i])
        if(!pointMap.has(points[i])){
            pointsUnused.push(points[i])
            console.log(pointsUnused)
        }
    }
    return pointsUnused;
}

function drawLines() {
    context.strokeStyle = 'red';
    context.lineWidth = 2;

    let leftAcetabular = pointMap.get("Left Acetabular");
    let leftFemoral = pointMap.get("Left Femoral Head");
    let rightFemoral = pointMap.get("Right Femoral Head");
    let rightAcetabular = pointMap.get("Right Acetabular");

    context.beginPath();
    context.moveTo(leftAcetabular.XPos, leftAcetabular.YPos);
    context.lineTo(leftFemoral.XPos, leftFemoral.YPos);
    context.stroke();

    context.beginPath();
    context.moveTo(leftFemoral.XPos, leftFemoral.YPos);
    context.lineTo(rightFemoral.XPos, rightFemoral.YPos);
    context.stroke();

    context.beginPath();
    context.moveTo(rightFemoral.XPos, rightFemoral.YPos);
    context.lineTo(rightAcetabular.XPos, rightAcetabular.YPos);
    context.stroke();
}

function drawArcs(angle1, angle2) {
    let leftAcetabular = pointMap.get("Left Acetabular");
    let leftFemoral = pointMap.get("Left Femoral Head");
    let rightFemoral = pointMap.get("Right Femoral Head");
    let rightAcetabular = pointMap.get("Right Acetabular");
    var angle1=calculateAngle(pointMap.get("Left Femoral Head"), pointMap.get("Left Acetabular"), pointMap.get("Right Femoral Head"))
    var angle2=calculateAngle(pointMap.get("Right Femoral Head"), pointMap.get("Right Acetabular"), pointMap.get("Left Femoral Head"))
    context.beginPath();

    let x= leftFemoral.XPos-leftAcetabular.XPos/10;
    let y= leftFemoral.YPos+leftAcetabular.YPos/10;
    let radius=20;
    let startAngle=0;
    let endAngle=angle1;
    context.arc(x, y, radius, startAngle, endAngle, 1);
}

var calculateAll = function (){
    let pointsLeftToSet = unsetPoints();
    console.log(pointsLeftToSet)
    if(pointsLeftToSet.length!==0){
        let message="Cannot calculate angles, points left unset:"
        for (i=0; i<pointsLeftToSet.length;i++){
            message+=pointsLeftToSet[i]+", ";
        }
        message = message.substr(0, message.length-2);
        document.getElementById("missing-points").innerHTML=message;
    } else {
        drawLines();
        drawArcs();
        document.getElementById("missing-points").innerHTML="";
        var angle1=calculateAngle(pointMap.get("Left Femoral Head"), pointMap.get("Left Acetabular"), pointMap.get("Right Femoral Head"))
        var angle2=calculateAngle(pointMap.get("Right Femoral Head"), pointMap.get("Right Acetabular"), pointMap.get("Left Femoral Head"))
        document.getElementById("Angle Left").innerHTML="Norberg angle for left hip is "+convertRadiansToDegrees(angle1) +" degrees";
        document.getElementById("Angle Right").innerHTML="Norberg angle for right hip is "+convertRadiansToDegrees(angle2) + " degrees";


    }
}


var Marker = function () {
    this.Sprite = new Image();
    this.Sprite.src = "http://www.clker.com/cliparts/w/O/e/P/x/i/map-marker-hi.png"
    this.Width = 12;
    this.Height = 20;
    this.XPos = 0;
    this.YPos = 0;
}

var Markers = new Array();

var mouseClicked = function (mouse) {
    // Get corrent mouse coords
    var rect = canvas.getBoundingClientRect();
    var mouseXPos = (mouse.x - rect.left);
    var mouseYPos = (mouse.y - rect.top);

    console.log("Marker added");

    // Move the marker when placed to a better location
    let currentMarker = document.querySelector('input[name="Current Marker"]:checked').value;

    var marker = new Marker();
    marker.XPos = mouseXPos //- (marker.Width / 2);
    marker.YPos = mouseYPos //- marker.Height;

    pointMap.set(currentMarker, marker);
}

// Add mouse click event listener to canvas
canvas.addEventListener("mousedown", mouseClicked, false);

var firstLoad = function () {
    context.font = "15px Georgia";
    context.textAlign = "center";
}

firstLoad();

var main = function () {
    draw();
    if(unsetPoints().length===0){
        drawLines()
    }
};

var draw = function () {
    // Clear Canvas
    context.fillStyle = "#000";
    context.fillRect(0, 0, canvas.width, canvas.height);

    // Draw map
    // Sprite, X location, Y location, Image width, Image height
    // You can leave the image height and width off, if you do it will draw the image at default size
    context.drawImage(mapSprite, 0, 0, 756, 755);

    // Draw markers
    for(let tempMarker of pointMap.values()){
        // Draw marker
        context.drawImage(tempMarker.Sprite, tempMarker.XPos-6, tempMarker.YPos-20, tempMarker.Width, tempMarker.Height);

        // Calculate postion text
        var markerText = "Postion (X:" + tempMarker.XPos + ", Y:" + tempMarker.YPos;

        // Draw a simple box so you can see the position
        var textMeasurements = context.measureText(markerText);
        context.fillStyle = "#666";
        context.globalAlpha = 0.7;
        //context.fillRect(tempMarker.XPos - (textMeasurements.width / 2), tempMarker.YPos - 15, textMeasurements.width, 20);
        context.globalAlpha = 1;

        // Draw position above
        context.fillStyle = "#000";
        //context.fillText(markerText, tempMarker.XPos, tempMarker.YPos);
    }
/*    for (var i = 0; i < Markers.length; i++) {
        var tempMarker = Markers[i];
        // Draw marker
        context.drawImage(tempMarker.Sprite, tempMarker.XPos, tempMarker.YPos, tempMarker.Width, tempMarker.Height);

        // Calculate postion text
        var markerText = "Postion (X:" + tempMarker.XPos + ", Y:" + tempMarker.YPos;

        // Draw a simple box so you can see the position
        var textMeasurements = context.measureText(markerText);
        context.fillStyle = "#666";
        context.globalAlpha = 0.7;
        context.fillRect(tempMarker.XPos - (textMeasurements.width / 2), tempMarker.YPos - 15, textMeasurements.width, 20);
        context.globalAlpha = 1;

        // Draw position above
        context.fillStyle = "#000";
        context.fillText(markerText, tempMarker.XPos, tempMarker.YPos);
    }*/
};

setInterval(main, (1000 / 60)); // Refresh 60 times a second

var calculateAngle = function (p1,p2,p3) {
    aX=p1.XPos-p2.XPos;
    aY=p1.YPos-p2.YPos;
    modA=Math.sqrt(aX*aX+aY*aY)

    bX=p1.XPos-p3.XPos;
    bY=p1.YPos-p3.YPos;
    modB=Math.sqrt(bX*bX+bY*bY)


    ratio=(aX*bY+aY*bY)/(modA*modB);

    angle=Math.acos(ratio);
    return angle;
}

var convertRadiansToDegrees = function (radians) {
    return 180/Math.PI *radians
}