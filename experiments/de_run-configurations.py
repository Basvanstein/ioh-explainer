from config import de_explainer

de_explainer.run(paralell=True, start_index=0, checkpoint_file="intermediate_de.csv")
de_explainer.save_results("de_final.pkl")
