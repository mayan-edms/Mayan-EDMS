'use strict';

QUnit.test('partialNavigation.filterLocation', function (assert) {
    var testPartialNavigation = new PartialNavigation({
        initialURL: '/testInitialURL',
    });

    /*
     * For an empty newLocation we expect the fragment of the URL minus the
     * query
     */
    var expected = new URI(new URI(location).fragment()).path().toString();
    assert.strictEqual(
        testPartialNavigation.filterLocation(''), expected, 'newLocation === ""');

    /*
     * For an empty root value we expect initialURL passed to the
     * partialNavigation instance when initialized.
     */
    assert.strictEqual(
        testPartialNavigation.filterLocation('/'), testPartialNavigation.initialURL, 'newLocation === "/"'
    );

    /*
     * For an empty root value we expect initialURL passed to the
     * partialNavigation instance when initialized.
     */
    assert.strictEqual(
        testPartialNavigation.filterLocation('random'), 'random', 'newLocation === "random"'
    );
});
