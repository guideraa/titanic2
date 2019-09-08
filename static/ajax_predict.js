
    function doPredictionAction1(){
            let predictionData = tagReferences.textareaObj.value;  // Text area where test data is displayed
            postRequest('/prediction', predictionData)
                .then(responseData => formatAndDisplayHTML(responseData, predictionData))
              .catch(error => console.error(error))

    }

    function displayTheError(errorMessage){
        alert(errorMessage);
    }

    /*
        Posts a json request to the given url.  The requestData param is a json string
        The response value is a json string
     */
    function postRequest(url, requestData) {
          return fetch(url, {
            method: 'POST',
            body: requestData,
            headers: new Headers({
              'Content-Type': 'application/json'
            }),
          })
          .then((response) => response.json()
          );
    }
    /*
        Format both the responseData and the predictData into an HTML table.
     */
    function formatAndDisplayHTML(responseData, predictData){
        //NOTE:  Returned data will be a json dict with a root label of "result"
        console.log("returned data: " + responseData);
        // Extract data from responseData and predictData for display in HTML table
        let json_dict = JSON.parse(responseData);  // dictionary
        let listResults = json_dict.result;  // list object of results just returned from model
        let predictDict = JSON.parse(predictData);  // dict object of prediction data used in model
        let age = predictDict.Age;
        let sex = predictDict.Sex;
        let embarked = predictDict.Embarked;
        // At this point, the lists listResult, age, sex, embarked are parallel lists"
        let returnHTML = "";
        returnHTML += "<table>";
        returnHTML += "<tr><td>Survived</td>" + "<td>Age</td>" + "<td>Sex</td>" + "<td>Embarked</td>"
        for(let i = 0; i < listResults.length; i++){
            returnHTML += "<tr>";
            returnHTML += "<td>" + listResults[i] + "</td>";
            returnHTML += "<td>" + age[i] + "</td>";
            returnHTML += "<td>" + sex[i] + "</td>";
            returnHTML += "<td>" + embarked[i] + "</td>";
            returnHTML += "</tr>";
        }
        returnHTML += "</table>";
        // Put HTML into the output div
        tagReferences.outputdivObj.innerHTML = returnHTML;
        tagReferences.outputdivObj.style.display = "block";
        return ;
    }
