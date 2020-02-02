//
//  MeatViewController.swift
//  MealME
//
//  Created by Tanay Kane on 2/1/20.
//  Copyright © 2020 Theodor Har. All rights reserved.
//

import UIKit

class MeatViewController: UIViewController {
    let repo = Repository()
    @IBAction func beefPressed(_ sender: Any) {
        API.ingredients.insert("beef")
    }
    
    @IBAction func fishPressed(_ sender: Any) {
        API.ingredients.insert("fish")
    }
    
    @IBAction func porkPressed(_ sender: Any) {
        API.ingredients.insert("pork")
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
