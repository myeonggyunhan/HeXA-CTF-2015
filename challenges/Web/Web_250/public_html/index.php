<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

$conn = mysqli_connect("localhost","web150","grantawish","web150");
?>
<html>
<head>
<title>Collect the dragon-balls.</title>
</head>
<body>
<h1>Collect the dragon-balls.</h1>
<form method=get action=index.php>
SELECT <input type=text onkeydown="if (event.keyCode == 13) { this.form.submit(); return false; }" size=50 name=query> <input value=" " type=submit>
<br>
<br>
[[MAP]] : d on d, r on r, a on a, g on g, o on o, n on n, b on b.
<br>
</form>
<?php
if (isset($_GET['query'])) {
    //echo "<br>SELECT $_GET[query]<br><br>";
    if(!preg_match("/^\D+$/",$_GET['query'])) 
        exit("Don't ask about number.");
    $q = mysqli_query($conn,"SELECT $_GET[query]") 
                   or die("Don't you know sql, Kakarot?");

    if (mysqli_num_rows($q) > 0) {
        echo "Dragonballs!<br>";
    } else {
        echo "I can't see any ball..<br>";
    }

    $s = 0;
    while($arr = mysqli_fetch_array($q)) {
        if (isset($arr['no'])) $s = $s + $arr['no'];
    }
    echo "The weight of the balls is .... $s<br><br>";
    if ($s == 800667) echo "I_wish_to_escape_solo_<br>";
}


?>
<br>
<br>
