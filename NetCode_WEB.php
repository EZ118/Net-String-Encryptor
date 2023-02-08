<?php

	header("content-type:text/html;charset=utf-8");

	$Current_Dict = "";
	$DefaultDict = "asdf1234ghjk5678lqwe90-=rtyu[]\;iopz',./xcvb`~!@nmMN#$%^BVCX&*()ZLKJ_+{}HGFD|:\"<SAQW>?ERTY UIOP";

	function encode($st){
		return base64_encode($st);
	}

	function decode($st){
		return base64_decode($st);
	}

	function hex2int($num){
		$num = hexdec($num);
		$num = number_format($num);
		return $num;
	}

	function int2hex($num){
		$ss = dechex($num);
		if (strlen($ss) < 2){
			$ss = "0" . $ss;
		}
		return $ss;
	}
	function CreateDict($url){
		$dic = "";
		$codes = file_get_contents($url);
		$codes = preg_replace('/([\x80-\xff]*)/i','',$codes);
		$codes = str_replace("\\n","",$codes);
		$codes = encode($url) . encode($codes) . $DefaultDict;
		$len = strlen($codes);

		for ($i = 0; $i < $len; $i ++){
			if (strpos($dic, $codes[$i]) !== false){
				continue;
			} else {
				$dic = $dic . $codes[$i];
			}
		}
		return $dic;
	}
	function NetEncode($dic, $txt){
		$final_txt = "";
		$orig_txt = encode($txt);
		$orig_txt_len = strlen($orig_txt);
		
		for ($i = 0; $i < $orig_txt_len; $i ++){
			if (strpos($dic, $orig_txt[$i]) !== false){
				$final_txt = $final_txt . int2hex( strpos($dic, $orig_txt[$i]) );
			} else {
				$final_txt = $final_txt . "**";
			}
		}
		
		$final_txt = encode($final_txt);
		return $final_txt;
	}

	function NetDecode($dic, $txt){
		$final_txt = "";
		$orig_txt = decode($txt);
		$orig_txt = str_replace("**", "", $orig_txt);
		$orig_txt_len = strlen($orig_txt);
		
		for ($i = 1; $i < $orig_txt_len; $i += 2){
			try{
				$final_txt = $final_txt . (string)( $dic[ hex2int( $orig_txt[$i - 1] . $orig_txt[$i] ) ] );
			} catch (Exception $e) {
				continue;
			}
		}
				
		$final_txt = decode($final_txt);
		return (string)$final_txt;
	}
?>


<?php
	@$ctype = $_REQUEST["ctype"];
	@$url = $_REQUEST["url"];
	@$txt = $_REQUEST["text"];

	if(!$url || !$txt || !$ctype) {
		echo("failed");
		die();
	}

	$Current_Dict = CreateDict($url);
	

	if ($ctype == "encode" || $ctype == "e") {
		echo( NetEncode($Current_Dict, $txt)) );
	} else {
		echo( NetDecode($Current_Dict, $txt) );
	}
	
?>

<?php
	/* 测试专用
	@$ctype = "e";
	@$url = "http://107.151.144.205/";
	@$txt = "测试";

	if(!$url || !$txt || !$ctype) {
		echo("failed");
		die();
	}

	$Current_Dict = CreateDict($url);
	

	if ($ctype == "encode" || $ctype == "e") {
		echo( NetEncode($Current_Dict, $txt) );
	} else {
		echo( NetDecode($Current_Dict, $txt) );
	}
	*/
?>
