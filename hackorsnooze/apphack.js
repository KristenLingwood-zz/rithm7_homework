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

$('.list-group').on('click', 'i', function(e) {
  console.log('hi');
  $(this).toggleClass('fas far');
  e.preventDefault();
});

//make all stories/favorites button show only specified class div items

//favorites button click should show only items with
