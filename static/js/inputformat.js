// Autoformatting provided by Cleave.js
// https://nosir.github.io/cleave.js/

/* global Cleave */
var date = new Cleave('.date-input', {
    date: true,
    delimiter: '-',
    dateMin: '1900-01-01',
    dateMax: '2099-12-01',
    datePattern: ['Y', 'm', 'd']
})

var time = new Cleave('.time-input', {
    time: true,
    timePattern: ['h', 'm']
})

var phone = new Cleave('.phone-input', {
    numeral: true,
    delimiter: ''
})