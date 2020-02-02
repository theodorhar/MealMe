//
//  OtherViewController.swift
//  MealME
//
//  Created by Tanay Kane on 2/1/20.
//  Copyright © 2020 Theodor Har. All rights reserved.
//

import UIKit

class OtherViewController: UIViewController {
    let repo = Repository()
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
    }
    
    @IBOutlet weak var textField: UITextField!
    
    @IBAction func buttonPressed(_ sender: Any) {
        API.ingredients.insert((textField.text as String?)!)
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
