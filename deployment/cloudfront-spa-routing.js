// CloudFront Function: viewer-request, runtime cloudfront-js-2.0.
// Attach only to the public website default cache behavior.
function handler(event) {
    var request = event.request;
    if (request.uri === '/portal' || request.uri.indexOf('/portal/') === 0) {
        return {statusCode: 404, statusDescription: 'Not Found'};
    }
    // The email-only launch no longer accepts form submissions.
    if (request.uri === '/thank-you' || request.uri === '/thank-you/') {
        return {statusCode: 302, statusDescription: 'Found',
                headers: {location: {value: '/#contact'}}};
    }
    var lastSegment = request.uri.substring(request.uri.lastIndexOf('/') + 1);
    if (lastSegment.indexOf('.') === -1) {
        request.uri = '/index.html';
    }
    return request;
}
