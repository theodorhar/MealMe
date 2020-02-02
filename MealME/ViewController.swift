//
//  ViewController.swift
//  MealME
//
//  Created by Theodor Har on 2/1/20.
//  Copyright © 2020 Theodor Har. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    
   // let repo = Repository()
    @IBOutlet weak var recipeCell: RecipeCell!
    var recipes: [[String: Any]] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        getRecipes()
    }
    
 
    func getRecipes() {
        let api = API()
        // Testing a sample list of ingredients
        
        api.getRecipes(ingredient_list: ["apples","flour","sugar"]) { recipes in
            if let recipes = recipes {
                print(recipes)
                self.recipes = recipes
                print(recipes)
                
            }
        }
    }    //let Image
    //cell.photoImageView.af_setImage(withURL:url)


}

