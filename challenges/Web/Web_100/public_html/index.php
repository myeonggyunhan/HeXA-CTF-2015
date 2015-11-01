<?php
    $buf = "";
    srand(time());
    for ($i=0; $i<100; $i++) {
        $r = rand()%1000+1;
        $buf = $buf."$r";
        $c = rand()%4;
        if ($c == 0) {
            $buf = $buf."+";
        } else if ($c == 1) {
            $buf = $buf."-";
        } else if ($c == 2) {
            $buf = $buf."*";
        } else if ($c == 3) {
            $buf = $buf."/";
        }
    }
    $r = rand()%1000+1;
    $buf = $buf."$r";

    $command = escapeshellcmd("python /home/web100/test.py $buf");
    $value = shell_exec($command);
    $value = substr($value,0,strlen($value)-1);

    //echo gettype($_GET[answer]);
    //echo gettype($value);
    if ($_GET) {
        echo "Your answer is $_GET[answer]<br>";
        echo "The right answer is $value<br>";
        if (strcmp($_GET['answer'],$value) == 0) {
            echo "You are a GO0O0OD_C0M_PUT3R\n";
        } else {
            //echo strlen($_GET['answer']);
            //echo strlen($value);
            //echo strcmp($_get['answer'],$value);
            echo "You are a human. Get away!\n";
        }
        exit;
    } else {
        echo $buf;
    }
?>
<br><br><br>
<h5> Hey you! Are you a MACHINE? </h5>
<p> The Turing test is a test of a machine's ability to exhibit intelligent behavior equivalent to, or indistinguishable from, that of a human. Alan Turing proposed that a human evaluator would judge natural language conversations between a human and a machine that is designed to generate human-like responses. The evaluator would be aware that one of the two partners in conversation is a machine, and all participants would be separated from one another. The conversation would be limited to a text-only channel such as a computer keyboard and screen so that the result would not be dependent on the machine's ability to render words as speech. If the evaluator cannot reliably tell the machine from the human (Turing originally suggested that the machine would convince a human 70% of the time after five minutes of conversation), the machine is said to have passed the test. The test does not check the ability to give correct answers to questions, only how closely answers resemble those a human would give. (https://en.wikipedia.org/wiki/Turing_test) </p>
<br>
<form action=index.php method=GET>
<input type=text name=answer /> <br/>
<input type=submit value="Submit"/> <br/>
</form>
