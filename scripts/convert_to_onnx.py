from ultralytics import YOLO
import argparse
import os

def convert_to_onnx(pt_model_path, output_dir=None, opset=12, simplify=True):
    if not os.path.exists(pt_model_path):
        raise FileNotFoundError(f"Model not found at: {pt_model_path}")

    print(f"✅ Loading YOLOv8 model from: {pt_model_path}")
    model = YOLO(pt_model_path)

    export_path = model.export(format="onnx", opset=opset, simplify=simplify)

    print(f"✅ Exported ONNX model to: {export_path}")

    return export_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert YOLOv8 .pt model to ONNX format")
    parser.add_argument("--pt", type=str, required=True, help="Path to the .pt file (YOLOv8 model)")
    parser.add_argument("--opset", type=int, default=12, help="ONNX opset version (default: 12)")
    parser.add_argument("--no-simplify", action="store_true", help="Don't simplify ONNX model")

    args = parser.parse_args()
    convert_to_onnx(
        pt_model_path=args.pt,
        opset=args.opset,
        simplify=not args.no_simplify
    )
