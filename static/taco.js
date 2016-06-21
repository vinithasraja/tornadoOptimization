   $("a.list_taco").click(function() {
      //get url, taco name and empty the table
    var url = $(this).attr('data-url');
    var taco = $(this).text();
    $('#goodtoppings').empty();
    $('#badtoppings').empty();

    //ajax request to get the taco information
    $.getJSON(url, function(data) {
      //update the count of good and bad toppings
      $('#good_badge').text(data['good_toppings'].length);
      $('#bad_badge').text(data['bad_toppings'].length);


      var good_topping_html = '';
      var bad_topping_html = '';

      //Good_topping list with toppings and ingredients with count
      var ingredients = '';
      for (var i=0; i < data['good_toppings'].length; i++) {
        good_topping_html += '<a href="#" class="list-group-item trying" data-index="' + i + '">' +
        '<span class="glyphicon">' +
        '<p class = "text-primary">' + data["good_toppings"][i]["topping_name"] + ' topping has ' + data["good_toppings"][i]["ingredients"].length + '   ingredients </p>'
        ingredients= data["good_toppings"][i]["ingredients"].join(" ")

        good_topping_html +=  ingredients + '</span></a>'
      }
      $("#goodtoppings").append(good_topping_html);

      //Bad_topping list with toppings and ingredients with count
      var ingredients = '';
      for (var i=0; i < data['bad_toppings'].length; i++) {
        bad_topping_html += '<a href="#" class="list-group-item" data-index="' + i + '">' +
        '<span style="word-break: break-word;" class="glyphicon">' +
        '<p class = "text-primary">' + data["bad_toppings"][i]["topping_name"] + ' topping has ' + data["bad_toppings"][i]["ingredients"].length + '   ingredients </p>'
        ingredients= data["bad_toppings"][i]["ingredients"].join(" ")

        bad_topping_html +=  ingredients + '</span></a>'
      }
      $("#badtoppings").append(bad_topping_html);
    });
  });