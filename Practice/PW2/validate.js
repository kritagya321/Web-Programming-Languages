window.onload = function(){

    //there will be one span element for each input field
    // when the page is loaded, we create them and append them to corresponding input element 
	// they are initially empty and hidden

    var span1 = document.createElement("span");
    var span2 = document.createElement("span2");
    var span3 = document.createElement("span3");
    var span4 = document.createElement("span4");

	span1.style.display = "none"; //hide the span element
    span2.style.display = "none";
    span3.style.display = "none";

	var email = document.getElementById("inputEmail");
    email.parentNode.appendChild(span1);


    var password = document.getElementById("inputpwd");
    password.parentNode.appendChild(span2);

    var confirm = document.getElementById("confirm")
    confirm.parentNode.appendChild(span3);

    var form = document.getElementById("myForm");
    
    email.onfocus = function(){
        span1.className = "none";
        span1.style.display="inline";
        span1.innerHTML = "Please enter a valid email address: abc@def.xyz";    
    }

    email.onblur = function(){
        span1.style.display = "none";
    }



    password.onfocus = function(){
        span2.className = "none";
        span2.style.display = "inline";
        span2.innerHTML = "Password should be atleast 6 character";
    }
    password.onblur = function(){
        span2.style.display = "none";
    }

    form.addEventListener('submit', (e)=>{
        var reg = /^([a-zA-Z0-9]+)@([a-zA-Z])+.([a-z]+)/
        if (email.value == '' || email.value == null || !(email.value.match(reg))){
            span1.className = "error";
            span1.style.display = "inline";
            span1.innerHTML = "Not a valid email address. Please re-enter";
            e.preventDefault()           
        }
        if (password.value == '' || password.value == null || password.value.length < 6){
            span2.className = "error";
            span2.style.display = "inline";
            span2.innerHTML = "Password should be atleast 6 character";
            e.preventDefault()
        }
        if (password.value != confirm.value){
            span2.className = "error";
            span3.className = "error";
            span2.style.display = "inline";
            span3.style.display = "inline";
            span2.innerHTML = "Password does not match";
            span3.innerHTML = "Password does not match";
            e.preventDefault()
        }


    })
 
}


    









