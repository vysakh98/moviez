	$("#ph").focus(function(){
	var ps=document.getElementById("psw1");
	console.log(ps);
	console.log("weak");
	if (ps.value.length<8){
	document.getElementById("weak").innerHTML ="weak password";
	}
	else{
		document.getElementById("weak").innerHTML ="";
	}
	
	});

	$(".btn").mouseover(function(){
		var ph=document.getElementById("ph");
		console.log(ph.value.length)
		if (ph.value.length<10){
			document.getElementById("weak2").innerHTML="invalid number"
		}
		else{
			document.getElementById("weak2").innerHTML=""
		}
	});


