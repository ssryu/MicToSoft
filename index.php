<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>MicToSoft</title>
        <script type="text/javascript" src="FunkyBlocks.js"></script>

        <?php wp_head(); ?>
    </head>
    <body>
        <audio src="sound.mp3" id="./FunkyBlocks/sound"></audio>
        <audio src="letsgo.mp3" id="./FunkyBlocks/bgm"></audio>
        <canvas id="canvas" width="800" height="600"></canvas>
        <img id="START" src="./FunkyBlocks/start.png" onclick="go()"><br/>
        <img id="bgimage" src="./FunkyBlocks/back.png" style="display:none" />
        <img id="block0" src="./FunkyBlocks/block0.png" style="display:none" />
        <img id="block1" src="./FunkyBlocks/block1.png" style="display:none" />
        <img id="block2" src="./FunkyBlocks/block2.png" style="display:none" />
        <img id="block3" src="./FunkyBlocks/block3.png" style="display:none" />
        <img id="block4" src="./FunkyBlocks/block4.png" style="display:none" />
        <h1>MicToSoft</h1>

        <p>サンプル</p>

        <script type="text/javascript">
            FunkyBlocks.init();
        </script>
        <?php wp_footer(); ?>
    </body>
</html>
