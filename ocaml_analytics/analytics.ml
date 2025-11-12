(* Analytics Module in OCaml *)
(* Functional implementation of market data analytics *)

(* Calculate mean of a float list *)
let mean (prices : float list) : float =
  match prices with
  | [] -> 0.0
  | _ ->
      let sum = List.fold_left (+.) 0.0 prices in
      let count = float_of_int (List.length prices) in
      sum /. count

(* Calculate variance *)
let variance (prices : float list) : float =
  let avg = mean prices in
  let squared_diffs = List.map (fun x -> (x -. avg) ** 2.0) prices in
  mean squared_diffs

(* Calculate standard deviation (volatility) *)
let std_dev (prices : float list) : float =
  sqrt (variance prices)

(* Calculate returns from prices *)
let calculate_returns (prices : float list) : float list =
  let rec aux acc = function
    | [] | [_] -> List.rev acc
    | p1 :: p2 :: rest ->
        let ret = (p2 -. p1) /. p1 in
        aux (ret :: acc) rest
  in
  aux [] prices

(* Calculate volatility from prices *)
let volatility_from_prices (prices : float list) (annualize : bool) : float =
  let returns = calculate_returns prices in
  let vol = std_dev returns in
  if annualize then
    vol *. sqrt 252.0  (* Annualize assuming 252 trading days *)
  else
    vol

(* Calculate minimum value *)
let min_value (prices : float list) : float =
  match prices with
  | [] -> 0.0
  | hd :: tl -> List.fold_left min hd tl

(* Calculate maximum value *)
let max_value (prices : float list) : float =
  match prices with
  | [] -> 0.0
  | hd :: tl -> List.fold_left max hd tl

(* Calculate total return *)
let total_return (prices : float list) : float =
  match prices with
  | [] -> 0.0
  | _ ->
      let first = List.hd prices in
      let last = List.hd (List.rev prices) in
      ((last -. first) /. first) *. 100.0

(* Calculate Sharpe ratio *)
let sharpe_ratio (returns : float list) (risk_free_rate : float) : float =
  let mean_return = mean returns in
  let std_return = std_dev returns in
  if std_return = 0.0 then
    0.0
  else
    let annual_mean = mean_return *. 252.0 in
    let annual_std = std_return *. sqrt 252.0 in
    (annual_mean -. risk_free_rate) /. annual_std

(* Calculate maximum drawdown *)
let max_drawdown (prices : float list) : float =
  let rec aux max_so_far min_dd = function
    | [] -> min_dd
    | price :: rest ->
        let new_max = max max_so_far price in
        let drawdown = (price -. new_max) /. new_max in
        let new_min_dd = min min_dd drawdown in
        aux new_max new_min_dd rest
  in
  match prices with
  | [] -> 0.0
  | hd :: tl -> aux hd 0.0 tl

(* Generate comprehensive analytics report *)
let generate_report (prices : float list) : (string * float) list =
  let returns = calculate_returns prices in
  [
    ("mean_price", mean prices);
    ("min_price", min_value prices);
    ("max_price", max_value prices);
    ("volatility_daily", volatility_from_prices prices false);
    ("volatility_annual", volatility_from_prices prices true);
    ("total_return", total_return prices);
    ("mean_return", mean returns);
    ("sharpe_ratio", sharpe_ratio returns 0.02);
    ("max_drawdown", max_drawdown prices);
  ]

(* JSON output helper *)
let print_json_report (report : (string * float) list) : unit =
  print_string "{\n";
  List.iteri (fun i (key, value) ->
    Printf.printf "  \"%s\": %.6f" key value;
    if i < List.length report - 1 then print_string ",\n" else print_string "\n"
  ) report;
  print_string "}\n"

(* Main function for standalone execution *)
let () =
  (* Example usage - can be extended to read from file *)
  if Array.length Sys.argv > 1 then
    try
      (* Read JSON file with prices *)
      let filename = Sys.argv.(1) in
      let ic = open_in filename in
      let json_str = really_input_string ic (in_channel_length ic) in
      close_in ic;
      
      (* Simple JSON parsing for array of floats *)
      (* Note: For production, use a proper JSON library like yojson *)
      let json_str = String.trim json_str in
      let json_str = 
        if String.length json_str > 0 && json_str.[0] = '[' then
          String.sub json_str 1 (String.length json_str - 2)
        else
          json_str
      in
      
      let price_strings = String.split_on_char ',' json_str in
      let prices = List.map (fun s -> float_of_string (String.trim s)) price_strings in
      
      let report = generate_report prices in
      print_json_report report
    with
    | _ ->
        Printf.eprintf "Error: Could not parse input file\n";
        exit 1
  else
    (* Demo with sample data *)
    let sample_prices = [100.0; 102.5; 101.8; 104.2; 103.5; 106.0; 105.5; 108.0; 107.2; 110.0] in
    Printf.printf "OCaml Analytics Module - Demo\n";
    Printf.printf "================================\n\n";
    Printf.printf "Sample prices: [";
    List.iter (Printf.printf "%.2f ") sample_prices;
    Printf.printf "]\n\n";
    
    let report = generate_report sample_prices in
    Printf.printf "Analytics Report:\n";
    print_json_report report
