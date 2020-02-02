//
//  APICaller.swift
//  MealME
//
//  Created by Theodor Har on 2/1/20.
//  Copyright © 2020 Theodor Har. All rights reserved.
//

import Foundation

class API {

    // Gets the posts json data and returns it converted as a dictionary
    func getRecipes(ingredient_list:[String] = [],completion: @escaping ([[String: Any]]?) -> Void) {
        // Network request snippet
        let ingredients = ingredient_list.joined(separator: "%252C")
        let urlString = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients?number=5&ranking=1&ignorePantry=false&ingredients=" + ingredients
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
                let responseDictionary = dataDictionary["response"] as! [String: Any]
                recipes = responseDictionary["posts"] as! [[String: Any]]
                
                return completion(recipes)
                
            }
        }
        task.resume()
        
    }

}
