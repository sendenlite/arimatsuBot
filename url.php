
<?php
$width=730;
$height=380;
$width2=880;
$height2=790;
$width3=750;
$height3=750;
$width4=350;
$height4=750;
$width5=250;
$height5=750;

$TokyoCode = array();
$TokyoOwn = array();
$AichiCode = array();
$AichiOwn = array();
$KanagawaCode = array();
$KanagawaOwn = array();
$SaitamaCode = array();
$SaitamaOwn = array();
$OsakaCode = array();
$OsakaOwn = array();


require 'initialize.php';

if($argv[1]=="1"){

$string = "https://map.yahooapis.jp/map/V1/static?width=$width&height=$height&lat=35.699372&lon=139.432747&z=11&appid=dj00aiZpPW1JSEhhelFObmM2aiZzPWNvbnN1bWVyc2VjcmV0Jng9Mzk-&mode=blankmap&style=bm.b.state:DC143C|";

    try {
        $pdo = new PDO('mysql:host=localhost;dbname=arimatsu;charset=utf8',MYSQL_USER,MYSQL_PASSWORD,
            array(PDO::ATTR_EMULATE_PREPARES => false));
    } catch (PDOException $e) {
         exit("\"\n<span class=\"warn\">データベースに接続できません。</span>\n<br>".date( "Y/m/d H:i.s", $_SERVER['REQUEST_TIME'])."\n<br><br>\n".$e->getMessage());
    }

    $stmt = $pdo -> prepare("select code, own from Tokyo");
    $stmt->execute();
    foreach ($stmt as $result){
        $TokyoCode[] = $result['code'];
        $TokyoOwn += array($result['code'] => $result['own']);
    }
    unset($result);
    for ($i=0;$i<count($TokyoCode);$i++) {
        if ($TokyoOwn[$TokyoCode[$i]]==1){
            $string .= "bm.p.${TokyoCode[$i]}:9370DB|";
        }
        if ($TokyoOwn[$TokyoCode[$i]]==2){
            $string .= "bm.p.${TokyoCode[$i]}:87CEFA|";
        }
    }

echo $string;
}elseif($argv[1]=="2"){


$string = "https://map.yahooapis.jp/map/V1/static?width=$width2&height=$height2&lat=35.006390&lon=137.247965&z=11&appid=dj00aiZpPW1JSEhhelFObmM2aiZzPWNvbnN1bWVyc2VjcmV0Jng9Mzk-&mode=blankmap&style=bm.b.state:DC143C|";

    try {
        $pdo = new PDO('mysql:host=localhost;dbname=arimatsu;charset=utf8',MYSQL_USER,MYSQL_PASSWORD,
            array(PDO::ATTR_EMULATE_PREPARES => false));
    } catch (PDOException $e) {
         exit("\"\n<span class=\"warn\">データベースに接続できません。</span>\n<br>".date( "Y/m/d H:i.s", $_SERVER['REQUEST_TIME'])."\n<br><br>\n".$e->getMessage());
    }

    $stmt = $pdo -> prepare("select code, own from Aichi");
    $stmt->execute();
    foreach ($stmt as $result){
        $AichiCode[] = $result['code'];
        $AichiOwn += array($result['code'] => $result['own']);
    }
    unset($result);
    for ($i=0;$i<count($AichiCode);$i++) {
        if ($AichiOwn[$AichiCode[$i]]==1){
            $string .= "bm.p.${AichiCode[$i]}:9370DB|";
        }
        if ($AichiOwn[$AichiCode[$i]]==3){
            $string .= "bm.p.${AichiCode[$i]}:FFA500|";
        }
        if ($AichiOwn[$AichiCode[$i]]==4){
            $string .= "bm.p.${AichiCode[$i]}:B0C4DE|";
        }
         if ($AichiOwn[$AichiCode[$i]]==5){
            $string .= "bm.p.${AichiCode[$i]}:ffd700|";
        }
    }

echo $string;

}elseif($argv[1]=="3"){



$string = "https://map.yahooapis.jp/map/V1/static?width=$width3&height=$height3&lat=35.145564&lon=136.913060&z=13&appid=dj00aiZpPW1JSEhhelFObmM2aiZzPWNvbnN1bWVyc2VjcmV0Jng9Mzk-&mode=blankmap&style=";

    try {
        $pdo = new PDO('mysql:host=localhost;dbname=arimatsu;charset=utf8',MYSQL_USER,MYSQL_PASSWORD,
            array(PDO::ATTR_EMULATE_PREPARES => false));
    } catch (PDOException $e) {
         exit("\"\n<span class=\"warn\">データベースに接続できません。</span>\n<br>".date( "Y/m/d H:i.s", $_SERVER['REQUEST_TIME'])."\n<br><br>\n".$e->getMessage());
    }

    $stmt = $pdo -> prepare("select code, own from Aichi");
    $stmt->execute();
    foreach ($stmt as $result){
        $AichiCode[] = $result['code'];
        $AichiOwn += array($result['code'] => $result['own']);
    }
    unset($result);

    for ($i=0;$i<count($AichiCode);$i++) {
        if ($AichiOwn[$AichiCode[$i]]==1){
            $string .= "bm.p.${AichiCode[$i]}:9370DB|";
        }
        if ($AichiOwn[$AichiCode[$i]]==3){
            $string .= "bm.p.${AichiCode[$i]}:FFA500|";
        }
        if ($AichiOwn[$AichiCode[$i]]==4){
            $string .= "bm.p.${AichiCode[$i]}:B0C4DE|";
        }
         if ($AichiOwn[$AichiCode[$i]]==5){
            $string .= "bm.p.${AichiCode[$i]}:3CB371|";
        }
    }

echo $string;


}elseif($argv[1]=="4"){


    
$string = "https://map.yahooapis.jp/map/V1/static?width=730&height=490&lat=35.407794&lon=139.353837&z=11&appid=dj00aiZpPW1JSEhhelFObmM2aiZzPWNvbnN1bWVyc2VjcmV0Jng9Mzk-&mode=blankmap&style=bm.b.state:DC143C|";

    try {
        $pdo = new PDO('mysql:host=localhost;dbname=arimatsu;charset=utf8',MYSQL_USER,MYSQL_PASSWORD,
            array(PDO::ATTR_EMULATE_PREPARES => false));
    } catch (PDOException $e) {
         exit("\"\n<span class=\"warn\">データベースに接続できません。</span>\n<br>".date( "Y/m/d H:i.s", $_SERVER['REQUEST_TIME'])."\n<br><br>\n".$e->getMessage());
    }

    $stmt = $pdo -> prepare("select code, own from Kanagawa");
    $stmt->execute();
    foreach ($stmt as $result){
        $KanagawaCode[] = $result['code'];
        $KanagawaOwn += array($result['code'] => $result['own']);
    }
    unset($result);
    for ($i=0;$i<count($KanagawaCode);$i++) {
        if ($KanagawaOwn[$KanagawaCode[$i]]==1){
            $string .= "bm.p.${KanagawaCode[$i]}:9370DB|";
        }
        if ($KanagawaOwn[$KanagawaCode[$i]]==2){
            $string .= "bm.p.${KanagawaCode[$i]}:87CEFA|";
        }
    }



echo $string;

}elseif($argv[1]=="5"){




$string = "https://map.yahooapis.jp/map/V1/static?width=880&height=490&lat=36.023130&lon=139.297834&z=11&appid=dj00aiZpPW1JSEhhelFObmM2aiZzPWNvbnN1bWVyc2VjcmV0Jng9Mzk-&mode=blankmap&style=bm.b.state:DC143C|";

    try {
        $pdo = new PDO('mysql:host=localhost;dbname=arimatsu;charset=utf8',MYSQL_USER,MYSQL_PASSWORD,
            array(PDO::ATTR_EMULATE_PREPARES => false));
    } catch (PDOException $e) {
         exit("\"\n<span class=\"warn\">データベースに接続できません。</span>\n<br>".date( "Y/m/d H:i.s", $_SERVER['REQUEST_TIME'])."\n<br><br>\n".$e->getMessage());
    }

    $stmt = $pdo -> prepare("select code, own from Saitama");
    $stmt->execute();
    foreach ($stmt as $result){
        $SaitamaCode[] = $result['code'];
        $SaitamaOwn += array($result['code'] => $result['own']);
    }
    unset($result);
    for ($i=0;$i<count($SaitamaCode);$i++) {
        if ($SaitamaOwn[$SaitamaCode[$i]]==1){
            $string .= "bm.p.${SaitamaCode[$i]}:9370DB|";
        }
        if ($SaitamaOwn[$SaitamaCode[$i]]==2){
            $string .= "bm.p.${SaitamaCode[$i]}:87CEFA|";
        }
    }

echo $string;

}elseif($argv[1]=="6"){




$string = "https://map.yahooapis.jp/map/V1/static?width=490&height=760&lat=34.663663&lon=135.419200&z=11&appid=dj00aiZpPW1JSEhhelFObmM2aiZzPWNvbnN1bWVyc2VjcmV0Jng9Mzk-&mode=blankmap&style=bm.b.state:DC143C|";


    try {
        $pdo = new PDO('mysql:host=localhost;dbname=arimatsu;charset=utf8',MYSQL_USER,MYSQL_PASSWORD,
            array(PDO::ATTR_EMULATE_PREPARES => false));
    } catch (PDOException $e) {
         exit("\"\n<span class=\"warn\">データベースに接続できません。</span>\n<br>".date( "Y/m/d H:i.s", $_SERVER['REQUEST_TIME'])."\n<br><br>\n".$e->getMessage());
    }

    $stmt = $pdo -> prepare("select code, own from Osaka");
    $stmt->execute();
    foreach ($stmt as $result){
        $OsakaCode[] = $result['code'];
        $OsakaOwn += array($result['code'] => $result['own']);
    }
    unset($result);
    for ($i=0;$i<count($OsakaCode);$i++) {
        if ($OsakaOwn[$OsakaCode[$i]]==6){
            $string .= "bm.p.${OsakaCode[$i]}:3CB371|";
        }
    }


echo $string;
}

?>

