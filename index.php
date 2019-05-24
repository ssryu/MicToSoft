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
    <script>
        var path = "<?php echo get_template_directory_url();?>";
    </script>
    <script src="<?php echo get_template_directory_url();?>/FunkyBlocks/FunkyBlocks.js"></script>

    <?php wp_head(); ?>
</head>
<body>

    <h1>MicToSoft</h1>

    <p>サンプル</p>

    <audio src="<?php echo get_template_directory_url();?>/FunkyBlocks/sound.mp3" id="sound"></audio>
    <audio src="<?php echo get_template_directory_url();?>/FunkyBlocks/letsgo.mp3" id="bgm"></audio>
    <canvas id="canvas" width="800" height="600"></canvas>
    <img id="START" src="<?php echo get_template_directory_url();?>/FunkyBlocks/start.png" onclick="go()"><br/>
    <img id="bgimage" src="<?php echo get_template_directory_url();?>/FunkyBlocks/back.png" style="display:none" />
    <img id="block0" src="<?php echo get_template_directory_url();?>/FunkyBlocks/block0.png" style="display:none" />
    <img id="block1" src="<?php echo get_template_directory_url();?>/FunkyBlocks/block1.png" style="display:none" />
    <img id="block2" src="<?php echo get_template_directory_url();?>/FunkyBlocks/block2.png" style="display:none" />
    <img id="block3" src="<?php echo get_template_directory_url();?>/FunkyBlocks/block3.png" style="display:none" />
    <img id="block4" src="<?php echo get_template_directory_url();?>/FunkyBlocks/block4.png" style="display:none" />

    <script type="text/javascript">
        FunkyBlocks.init();
    </script>
    <?php wp_footer(); ?>
</body>
</html>
