<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>MicToSoft</title>
        <script type="text/javascript" src="FunkyBlocks.js"></script>

        <?php wp_head(); ?>
    </head>
    <body>
        <audio src="sound.mp3" id="sound"></audio>
        <audio src="letsgo.mp3" id="bgm"></audio>
        <canvas id="canvas" width="800" height="600"></canvas>
        <img id="START" src="start.png" onclick="go()"><br/>
        <img id="bgimage" src="back.png" style="display:none" />
        <img id="block0" src="block0.png" style="display:none" />
        <img id="block1" src="block1.png" style="display:none" />
        <img id="block2" src="block2.png" style="display:none" />
        <img id="block3" src="block3.png" style="display:none" />
        <img id="block4" src="block4.png" style="display:none" />
        <h1>MicToSoft</h1>

        <p>サンプル</p>

        <script type="text/javascript">
            init();
        </script>
        <?php wp_footer(); ?>
    </body>
</html>
