  import streamlit as st
from PIL import Image
import math

def calculate_box_fit(large_box_length, large_box_width, large_box_height, small_box_length, small_box_width, small_box_height):

  num_fit_length = math.floor(large_box_length / small_box_length)
  num_fit_width = math.floor(large_box_width / small_box_width)
  num_fit_height = math.floor(large_box_height / small_box_height)

  return num_fit_length * num_fit_width * num_fit_height

pallet = (900, 1200, 1200)#Length x Width x Height
drawer = (450, 300, 300)#Length x Width x Height

st.set_page_config(page_title="Fulfilment Calculator", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")
st.write("🚚 Genuine Inside (M) Sdn. Bhd.")

st.title("Fulfilment Calculator 🧮")

"__________________________________________________________________________________________________________________________"
weight = st.selectbox("Product Weight", ["below 1kg", "1kg to 2.99kg", "3kg to 10kg", "above 10kg"], index=None)
colA, colB, colC = st.columns([1,1,1])
with colA:
    length = st.number_input("Length (mm):", value=0)
with colB:
    width = st.number_input("Width (mm):", value=0)
with colC:
    height = st.number_input("Height (mm):", value=0)
stock = st.number_input("Current Stock:", value=0)
inbound = st.number_input("Upcoming Inbound:", value=0)
orders = st.number_input("Orders per Month:", value=0)
material = st.multiselect("Packing material", ["Box", "Bubble Wrap", "Mailer"])
delivery = st.toggle("Delivery")
delivery_option = None
delivery_charge = 0
if delivery:
    delivery_option = st.selectbox("Delivery To:", ["West Malaysia", "East Malaysia"])
_ ,colA = st.columns([10,1])
with colA:
    submitted = st.button('Calculate')

if submitted:
    if weight == None or length <= 0 or width <= 0 or height <= 0:
        st.error('Weight/Length/Width/Height cannot be zero', icon="🚨")
        st.stop()
    "__________________________________________________________________________________________________________________________"
    item_per_pallet = calculate_box_fit(*pallet, *(length, width, height))
    "Item per Pallet", item_per_pallet
    if item_per_pallet <= 0:
        item_per_pallet = 1
    storage_rate=(stock+inbound-orders)/(item_per_pallet)*1.5*30

    if weight == "below 1kg":
        inbound_charge=inbound*1
        handling_charge=orders*1
        if delivery_option == "West Malaysia":
            delivery_charge=orders*6.5
        elif delivery_option == "East Malaysia":
            delivery_charge=orders*15

    elif weight == "1kg to 2.99kg":
        inbound_charge=inbound*2
        handling_charge=orders*2
        if delivery_option == "West Malaysia":
            delivery_charge=orders*8.10
        elif delivery_option == "East Malaysia":
            delivery_charge=orders*45

    elif weight == "3kg to 10kg":
        inbound_charge=inbound*3
        handling_charge=orders*3
        if delivery_option == "West Malaysia":
            delivery_charge=orders*10.30
        elif delivery_option == "East Malaysia":
            delivery_charge=orders*75

    elif weight == "above 10kg":
        inbound_charge=inbound*4
        handling_charge=orders*4
        if delivery_option == "West Malaysia":
            delivery_charge=orders*15.80
        elif delivery_option == "East Malaysia":
            delivery_charge=orders*150

    material_cost=0
    if "Box" in material:
        material_cost=material_cost+(orders*1)
    if "Bubble Wrap" in material:
        material_cost=material_cost+(orders*1)
    if "Mailer" in material:
        material_cost=material_cost+(orders*1)

    estimated_total=inbound_charge+storage_rate+handling_charge+material_cost+delivery_charge

    "#"
    colA, _ , colB = st.columns([4,22,3])
    with colA:
        "Inbound Charges"
        "Storage Charges"
        "Handling Charges"
        "Packing Material Cost"
        if delivery:
            "Delivery Charges"
    with colB:
        f"RM {inbound_charge:.2f}"
        f"RM {storage_rate:.2f}"
        f"RM {handling_charge:.2f}"
        f"RM {material_cost:.2f}"
        if delivery:
            f"RM {delivery_charge:.2f}"
    colA, _ , colB = st.columns([5,10,3])
    with colA:
        st.header("Estimated Total")
    with colB:
        st.header(f" RM {estimated_total:.2f}")

"__________________________________________________________________________________________________________________________"
fulfilment_image1 = Image.open("Fulfilment Rate.pptx_page-0001.jpg")
fulfilment_image2 = Image.open("Fulfilment Rate.pptx_page-0002.jpg")
__, colA, __ = st.columns([1,2,1])
with colA:
    st.image(fulfilment_image1, use_column_width=True)
    st.image(fulfilment_image2, use_column_width=True)
