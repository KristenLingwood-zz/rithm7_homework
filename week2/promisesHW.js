// Make a request to https://swapi.co/api/ and then log the response to the console. This tells you what kinds of data are stored in the API.
$.getJSON('https://swapi.co/api/', response => console.log(response));

// Make a request to the /films/ endpoint, and log out the names of all of the names and directors of the Star Wars films (it's okay if you log the same name more than once.) They should be in the format FILM_NAME - FILM_DIRECTOR.
let titleDirector = [];

for (let i = 1; i < 8; i++) {
  titleDirector.push($.getJSON(`https://swapi.co/api/films/${i}/`));
}

Promise.all(titleDirector)
  .then(movie => movie.forEach(m => console.log(`${m.title} - ${m.director}`)))
  .catch(err => console.log(err));

// Make a request to the first planet. Once you get the response, make a request to get information on each of that planet's residents. Once you get THAT information back, log out the name of every resident for that first planet.
$.getJSON(`https://swapi.co/api/planets/1/`)
  .then(res => {
    let planet = res;
    let planetRes = planet.residents;
    return Promise.all(planetRes.map(res => $.getJSON(res)));
  })

  .then(res => res.forEach(val => console.log(val.name)))
  .catch(err => console.log(`only droids here`, err));

// It's a fight for the galaxy! Race two requests: one to the 1st person, and one to the 4th person (based on their ids). If the request to the 1st person is processed first, log a message stating that the 1st person has saved the galaxy. Otherwise, log a message that the galaxy has fallen to the 4th person.

var luke = $.getJSON('https://swapi.co/api/people/1');
// .then(person => person.name)
// .catch(err => console.log(err));
var vader = $.getJSON('https://swapi.co/api/people/4');
// .then(person => person.name)
// .catch(err => console.log(err));

Promise.race([luke, vader])
  .then(winner => {
    if (winner.name === 'Luke Skywalker') {
      console.log(`${winner.name} has saved the galaxy!`);
    } else {
      throw new Error(`The galaxy has fallen to ${winner.name}`);
    }
  })
  .catch(err => console.log(err));
