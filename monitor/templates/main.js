var text = ["text1", "tex2", "text3", "text4"];
alert("running")

axios.get('/')
	.then( (res) =>{
		console.log(res)
	})

text.forEach(function(el) {
    var div = document.createElement("div");
    div.className = "finalBlock";
    div.innerHTML = getHtml(el);
    document.body.appendChild(div);
});