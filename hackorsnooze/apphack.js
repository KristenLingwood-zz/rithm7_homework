//handle submit with input and populate list
let listNum = 1;
$('#submitForm').submit(function(e) {
  e.preventDefault();

  let newStory = $('#title').val();
  let storyLink = $('#url').val();

  //add list item and button to ul

  $('#list').append(
    `<div class='story-list-item list-group-item' <li class="list-group-item"><i class="far fa-star"></i><a href=${storyLink}>${newStory}</a></li></div>`
  );

  //clear form
  $('#title').val('');
  $('#url').val('');
  listNum++;
});

//star changes to indicate favorite
$('.list-group').on('click', 'i', function(e) {
  console.log('hi');
  $(this).toggleClass('fas far');
  e.preventDefault();
});

//favorites button click should show only favorites
$('header').on('click', '#favorites', function(e) {
  $('.far')
    .closest('div')
    .hide();
  e.preventDefault();
});

//all stories shows all
$('header').on('click', '#allstories', function(e) {
  $('.far')
    .closest('div')
    .show();
  e.preventDefault();
});
