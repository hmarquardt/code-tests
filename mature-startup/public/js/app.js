function buildValoreImgURL(isbn) {
   var baseURL = 'https://img.valorebooks.com/FULL/';
   var pattern = /^([0-9]{2})([0-9]{2})([0-9]{2})([0-9]+)$/;
   var c = pattern.exec(isbn);
   return baseURL+c[1]+'/'+c[1]+c[2]+'/'+c[1]+c[2]+c[3]+'/'+c[0]+'.jpg';
}

$(function() {
   $('#isbnsubmit').click( function(e) {
	e.preventDefault();
	$('#results').empty();
	$.ajax({
           type: 'POST',
           url: '/api.php',
           data: {isbns: $('#isbns').val()},
           success:  function(data) {
	       var template = _.template($('#resultsTemplate').html());
	       var errtemplate = _.template($('#errorTemplate').html());
	       var prices = data.response.prices;
	       if(data.response.status) {
	          $('#results').html(errtemplate({msg: data.response.errmsg}));
	       } else {
	          $('#results').html(template({prices: prices}));
	       }
	       $('img').error(function() { $(this).unbind("error").
	         attr("src","https://img.valorebooks.com/images/book_coverW120.png")});
	       },
           error:  function(XMLHttpRequest, textStatus, errorThrown) {
		var errtemplate = _.template($('#errorTemplate').html());
		$('#results').html(errtemplate({msg: '<h3>A network or API failure has occured, please try later</h3>'}));
           }});
   }); 
});
