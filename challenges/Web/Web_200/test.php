<?php
error_reporting(E_ALL); ini_set('display_errors', '1');
$connect = mysqli_connect("localhost","web100","geniusyisang") or die("Mysql failed");
$db_con = mysqli_select_db($connect,"web100") or die("database connection error");
$q=mysqli_fetch_array(
	mysqli_query("select * from users")
	) or die("Nothing.");
echo "no : ".$q['no']." / ".$q['id'];
?>
