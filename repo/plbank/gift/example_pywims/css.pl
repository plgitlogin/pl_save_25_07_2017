<link rel="stylesheet" href="{% static 'css/pywims_exos.css' %}">
	<script type="text/x-mathjax-config">
	MathJax.Hub.Config({
		tex2jax: {
			inlineMath: [ ['$','$'], ["\\(","\\)"] ],
			displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
			processEscapes: true,
		},
		menuSettings: { inTabOrder : false }
	});
	</script>
	<script type="text/javascript"
	src="https://cdn.rawgit.com/mathjax/MathJax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
	</script>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

	<script>
	function allowDrop(ev) {
	    ev.preventDefault();
	}
	function drag(ev) {
	    ev.dataTransfer.setData("text", ev.target.id);
	}
	function drop(ev, target) // target est l'id de la source du drop
	{
		ev.preventDefault();

		if (!ev.target.getAttribute("ondrop")) return false;
		// data est l'id de la cible du drop
		var data=ev.dataTransfer.getData("text");
		// Le drop
		document.getElementById(target).appendChild(document.getElementById(data));
		// Renseignement de la variable via un champ "input" caché, dont l'id est celle le la cible, préfacée par 'input_'
		var input=document.getElementById('input_'+data);
		if (target != undefined) input.value = target;
		if (target == undefined) input.value = '';
	}
	</script>
{% endblock %}

{% block enonce %}
    <script>
    $( document ).ready(function(){
        if(window.top != window.self) {
            $('#home-link').remove();
        }
    });
    </script>

    <div class='exo'>
        {# <!-- {% url 'corrige_exo' %}--> #}
        <form action="" id = "form_exo" method="post" autocomplete = "off">
            <div class='form-enonce'>
                {% block enonce_exo %}{% endblock %}
            </div>

            <center><input class = 'btn btn-primary btn-lg' type=submit value=Valider></center>
        </form>
    </div>
{% endblock %}
