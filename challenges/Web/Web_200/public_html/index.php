<?php
//error_reporting(E_ALL); ini_set('display_errors', '1');

$conn = mysqli_connect("localhost","web100","geniusyisang","web100");
?>
<html>
<head>
<title>Find 13th.</title>
</head>
<body>
<h1>Find 13th.</h1>
<form method=get action=index.php>
ID: <input type=text onkeydown="if (event.keyCode == 13) { this.form.submit(); return false; }" name=id> <input value=" " type=submit>
</form>
<?php
if (isset($_GET['id'])) {
    if(preg_match("/union|from/",$_GET['id'])) 
        exit("What are you asking?");

    //echo "select * from users where id='$_GET[id]'<br><br>";
    $q=@mysqli_fetch_array(mysqli_query($conn,"select * from users where id='$_GET[id]'")) or die("Nothing.");
}
?>
</body>
