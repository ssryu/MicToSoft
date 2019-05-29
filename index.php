<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>MicToSoft</title>

    <style>
        #canvas {
            width: 800px;
            height: 600px;
            touch-action: none;
        }
        #START {
            position: absolute;
            left: 200px;
            top: 200px;
        }
    </style>
    <script src="/FunkyBlocks/FunkyBlocks.js"></script>
    <script src="brython.js"></script>
    <script src="brython_stdlib.js"></script>    
</head>
<body onload = "init();brython()">
    <audio src="/FunkyBlocks/sound.mp3" id="sound"></audio>
    <audio src="/FunkyBlocks/letsgo.mp3" id="bgm"></audio>
    <canvas id="canvas" width="800" height="600"></canvas>
    <img id="START" src="/FunkyBlocks/start.png" onclick="go()"><br/>
    <img id="bgimage" src="/FunkyBlocks/back.png" style="display:none" />
    <img id="block0" src="/FunkyBlocks/block0.png" style="display:none" />
    <img id="block1" src="/FunkyBlocks/block1.png" style="display:none" />
    <img id="block2" src="/FunkyBlocks/block2.png" style="display:none" />
    <img id="block3" src="/FunkyBlocks/block3.png" style="display:none" />
    <img id="block4" src="/FunkyBlocks/block4.png" style="display:none" />
    <!-- <div>
    <script type="text/javascript">
        init();
    </script>
    </div> -->

    <h1>MicToSoft</h1>

    <p>サンプル</p>

    <script type="text/python" src="bmi.py"></script>
    <h1>BrythonでBMIを計算する</h1>

    <p>身長(メートル)
    <input type="text" id="height" />
    <p>体重(キログラム)
    <input type="text" id="weight" />
    <br><button id="execute">計算だ!</button>

    <div id="result"></div>
</body>
</html>
