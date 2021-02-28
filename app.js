const express = require("express");
const app = express();
const port = 3000;
var fs = require("fs");

app.use(express.static(__dirname + "/public"));

app.get("/", (req, res) => {
  res.render("index.ejs");
});

app.get("/predictDate", function (req, res) {
  var date = new Date(req.query.date).getTime() / 1000;
  var obj = JSON.parse(fs.readFileSync("Df.json"));
  var datePrediction = obj.filter(function (obj) { return obj.ds == date;})
  datePrediction == "" ? res.redirect("/") :  res.render("index.ejs", { prediction : datePrediction[0].yhat, dateValue: req.query.date.toString()});
});

app.listen(process.env.PORT || port, () => {
  console.log(`Such listening at http://localhost:${port}`);
});
 