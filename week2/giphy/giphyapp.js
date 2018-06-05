$('.form-group').on('click', '#search', function(e) {
  e.preventDefault();
  let $searchTerm = $('#searchterm').val();
  $.getJSON(
    `https://api.giphy.com/v1/gifs/search?q=d${$searchTerm}&api_key=26JdhLStl0RSgP5KcycfOifzSiOlpa3T`,

    function(response) {
      console.log(response.data[0].images.fixed_height.url);
      let giphy = response.data[0].images.fixed_height.url;

      $('.container').append(`<img src=${giphy}>`);
      // $('.container').append(`<img src="http://lorempixel.com/400/200">`);
    }
  );
  $('#searchterm').val('');
});

$('.form-group').on('click', '#remove', function() {
  console.log('empty');
  $('.container').empty();
});

//to do: format input to be centered
//edge case of no giphy at data[0]
