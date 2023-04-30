describe('Logging into the system', () => {
  let uid // user id
  let email // email of the user
  let title // title of the task

  //  ###
  //    SETUP
  //          ###
  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          email = user.email
        })
      })

  })

  //  ###
  //    SETUP 2
  //        ###
  before(function () {
    // create a fabricated task from a fixture
    cy.fixture('task.json')
      .then((task) => {
        task.userid = uid
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: task
        }).then((response) => {
          title = task.title
        })
      })
  })

  //         ###
  //     PRE CONDITIONS
  //          ###
  beforeEach(function () {
    // enter the main page
    cy.visit('http://localhost:3000')

    // PRECONDITION 1 - Usr autenticated

    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
    // submit the form on this page
    cy.get('form')
      .submit()
    // assert that the user is now logged in

    // PRECONDITION 2 - At least 1 task created
    // Happens in fixture (task.json)

    // PRECONDITION 3 - views the created task in detail view mode
    cy.contains('div', title)
      .click()

  })

  //  Now all the preconditions are set. We have logged in with auth user. 
  //  We have created a task and we have clicked on it so it shows in detail view mode
  //  Now lets start the tests.

  // ### RBUC1





















  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
