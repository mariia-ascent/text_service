'use strict';
/* global eopti */

(async function() {

  await require('eopti/ms/ms_lib.js');


  // -1- define forward, i.e. the coordinates of python service
  //     we need to *de*-code its response, because a  handler is
  //     supposed to return an unencoded 
  async function forward(endpoint, message) {

    try {

      if (typeof message === 'undefined') message = {};
      message = JSON.stringify(message);
      message = Buffer.from(message, 'binary').toString('base64');

      let request = {
        hostname : 'localhost',
        port : 8090,
        path : endpoint
      };

      let response = await eopti.ms.http_send(request, message);
      response = momo.http_.atob(response);
      response = JSON.parse(response);
      return response;

    } catch (errorMsg) {
      throw `${errorMsg} <pre> << proxy.js::forward(${endpoint},message)`;
    }
  }


  // -2- connect the two endpoints in the python service, both via a definition of myHandlers
  //     and via a definition of myProxies. A handler shall consume and return plain json,
  //     a proxy is (here) simpler and more efficient, since it expects and returns
  //     base64 encode json
  let myHandlers = {

    "predict_handler" : async function(message){return await forward("/predict", message);}

  };

  let myProxies = {

    "predict_proxy" : {"portNo" : 8090, "urlPath" : "/predict" }

    };

  await eopti.ms.start(myHandlers, myProxies);

})();

