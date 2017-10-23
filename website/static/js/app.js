var auto = new autoComplete({
    selector: 'input.search',
    minChars: 1,
    source: function(term, suggest){
        $.get('/static/text/result7.txt', { q: term }, function(data){
            var choices = data.split("\n");
            var matches = [];
            for (i=0; i<choices.length; i++)
                if (~choices[i].toLowerCase().indexOf(term)) matches.push(choices[i]);
            suggest(matches);

        });

    }
});


console.log(auto);