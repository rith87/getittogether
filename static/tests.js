function parse_notes(notes)
{
    var parsedNotes = notes.split(";");
    parsedNotes.splice(parsedNotes.length - 1, 1);
    return parsedNotes;
}

// test( "hello test", function() {
    // ok( 1 == "1", "Passed!" );
// });

test( "parse notes", function() {
    var notes = '{"src":"http://127.0.0.1:5000/_uploads/screenshots/testImage_59.jpg", \
        "text":"rar","shapes":[{"type":"rect","geometry":{"x":0.46825396825396826,"width":0.17301587301587307,"y":0.40275650842266464,"height":0.12098009188361403}}], \
        "context":"http://127.0.0.1:5000/add"};{"src":"http://127.0.0.1:5000/_uploads/screenshots/testImage_59.jpg","text":"ow","shapes":[{"type":"rect","geometry":{"x":0.0746031746031746,"width":0.2492063492063492,"y":0.3660030627871363,"height":0.24502297090352226}}], \
        "context":"http://127.0.0.1:5000/add"};';
    var note0 = '{"src":"http://127.0.0.1:5000/_uploads/screenshots/testImage_59.jpg", \
        "text":"rar","shapes":[{"type":"rect","geometry":{"x":0.46825396825396826,"width":0.17301587301587307,"y":0.40275650842266464,"height":0.12098009188361403}}], \
        "context":"http://127.0.0.1:5000/add"}';
    var note1 = '{"src":"http://127.0.0.1:5000/_uploads/screenshots/testImage_59.jpg","text":"ow","shapes":[{"type":"rect","geometry":{"x":0.0746031746031746,"width":0.2492063492063492,"y":0.3660030627871363,"height":0.24502297090352226}}], \
        "context":"http://127.0.0.1:5000/add"}';
    var parsedNotes = parse_notes(notes);
    ok( parsedNotes.length == 2, "Length checked!" );
    ok( parsedNotes[0] == note0, "First entry checked!" );
    ok( parsedNotes[1] == note1, "Second entry checked!" );
});