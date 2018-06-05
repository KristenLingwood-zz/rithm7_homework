const $giphyHolder = $('.giphy-holder');
const $searchTerm = $('#searchterm').val();

$('.form-group').on('click', '#search', function(e) {
  let $giphy = $.get(
    `https://api.giphy.com/v1/gifs/search?q=dogs&api_key=26JdhLStl0RSgP5KcycfOifzSiOlpa3T`,

    function(response) {
      console.log(response.data[0].embed_url);
      response.data[0].embed_url;
    }
  );
  $giphyHolder.append(`<img src=${$giphy}>`);
  $('#searchterm').empty();
  e.preventDefault();
});

$('.form-group').on('click', '#remove', function() {
  console.log('empty');
  $giphyHolder.empty();
});
