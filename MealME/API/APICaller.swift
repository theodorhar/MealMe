//
//  APICaller.swift
//  MealME
//
//  Created by Theodor Har on 2/1/20.
//  Copyright © 2020 Theodor Har. All rights reserved.
//

import Foundation

class API {
    static var ingredients:Set<String> = ["apple","flour","sugar"]
    let url_base = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"
    // Gets the posts json data and returns it converted as a dictionary
    let headers = [
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": "0203654c27mshf4fe4fcfc155983p1bb69fjsn7ed59b996765"
    ]
    

    func getRecipes(ingredient_list:[String],completion: @escaping ([[String: Any]]?) -> Void) {
        // Network request snippet
        let ingredient_set = ingredient_list.joined(separator: "%252C")
        let urlString = url_base + "findByIngredients?number=5&ranking=1&ignorePantry=false&ingredients=" + ingredient_set
        let url = URL(string: urlString)!
        var request = URLRequest(url:url)
        request.setValue("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com", forHTTPHeaderField: "x-rapidapi-host")
        request.setValue("0203654c27mshf4fe4fcfc155983p1bb69fjsn7ed59b996765", forHTTPHeaderField: "x-rapidapi-key")
        print(request)
        let session = URLSession(configuration: .default, delegate: nil, delegateQueue: OperationQueue.main)
        session.configuration.requestCachePolicy = .reloadIgnoringLocalCacheData
        let task = session.dataTask(with: request) { (data, response, error) in
            if let error = error {
                print(error.localizedDescription)
            } else if let data = data,
               
                // Where data comes from API in JSON Format
                let dataDictionary = try! JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                
               
                print(dataDictionary)
                // Actual Dict that stores info nicely
                var recipes: [[String: Any]] = []
                
                // Get the posts and return them
                // I believe it returns a string so
                //as! [[String: Any]]
                let responseDictionary = dataDictionary as! [[String:Any]]

                recipes = responseDictionary as! [[String: Any]]

                return completion(recipes)
                
            }
        }
        task.resume()
        
    }

    
    func getRecipeInfo(id:Int,completion: @escaping ([[String: Any]]?) -> Void) {
        // Network request snippet
        
        let urlString = url_base + "findByIngredients?number=5&ranking=1&ignorePantry=false&ingredients=" + String(id) + "/information"
        let url = URL(string: urlString)!
        let session = URLSession(configuration: .default, delegate: nil, delegateQueue: OperationQueue.main)
        session.configuration.requestCachePolicy = .reloadIgnoringLocalCacheData
        let task = session.dataTask(with: url) { (data, response, error) in
            if let error = error {
                print(error.localizedDescription)
            } else if let data = data,
                
                
                // Where data comes from API in JSON Format
                let dataDictionary = try! JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                
               
            
                // Actual Dict that stores info nicely
                var recipes: [[String: Any]] = []
                
                // Get the posts and return them
                // I believe it returns a string so
                let responseDictionary = dataDictionary as! [[String: Any]]
                recipes = responseDictionary[0] as! [[String: Any]]
                
                return completion(recipes)
                
            }
        }
        task.resume()
        
    }
}
