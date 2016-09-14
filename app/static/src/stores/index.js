const redux = require('redux');
const reducers = require('../reducers');

module.exports = function(initialState) {
  const store = redux.createStore(reducers, initialState)

  return store
}
