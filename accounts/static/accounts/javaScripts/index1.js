d3.csv("smartHealthPortal/accounts/static/accounts/javaScripts/data.csv", function(myarray){
    myarray.forEach(function (d) {
    console.log(d.date + "," + d.close);
    });
    });


     <script type="text/javascript" src="{% static 'accounts/javaScripts/index1.js' %}"></script>