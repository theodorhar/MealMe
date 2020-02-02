//
//  PlantViewController.swift
//  MealME
//
//  Created by Tanay Kane on 2/1/20.
//  Copyright © 2020 Theodor Har. All rights reserved.
//

import UIKit

class PlantViewController: UIViewController {
    let repo = Repository()
    @IBAction func potatoButton(_ sender: Any) {
        API.ingredients.insert("potato")
    }
    
    @IBAction func tomatoPressed(_ sender: Any) {
        API.ingredients.insert("tomato")
    }
    @IBAction func lettucePressed(_ sender: Any) {
        API.ingredients.insert("lettuce")
    }
    
    @IBAction func garlicPressed(_ sender: Any) {
        API.ingredients.insert("garlic")
    }
    
    @IBAction func onionPressed(_ sender: Any) {
        API.ingredients.insert("onion")
    }
    @IBAction func zucchiniPressed(_ sender: Any) {
        API.ingredients.insert("zucchini")
    }
    
    @IBAction func carrotPressed(_ sender: Any) {
        API.ingredients.insert("carrot")
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print(API.ingredients)
        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
