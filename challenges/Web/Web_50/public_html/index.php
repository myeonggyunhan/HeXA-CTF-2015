<?php
if ($_POST) {
    if ($_POST['id'] == "John Smith" && $_POST['pw'] == "hexahexaiamhexa") {
        echo "The flag is : Winter_12_comming\n";
        exit;
    } else {
        echo "WRONG\n";
        exit;
    }
}
?>

<form action=. method=POST>
<input type=text name=id value="ID" onkeydown="this.value='';" onkeyup="this.value='';" onMouseover="this.style.left = Math.random()*500; this.style.top= Math.random()*500;" style="position:absolute;" tabindex=-1 /> <br/>
<input type=password name=pw value="password"  onkeydown="this.value='';" onkeyup="this.value='';" onMouseover="this.style.left = Math.random()*500; this.style.top= Math.random()*500;" style="position:absolute;" tabindex=-1 /> <br/>
<input type=submit value="OK" onMouseover="this.style.left = Math.random()*500; this.style.top= Math.random()*500;" style="position:absolute;" />
</form>
