function varargout = Arayuz(varargin)
%ARAYUZ MATLAB code file for Arayuz.fig
%      ARAYUZ, by itself, creates a new ARAYUZ or raises the existing
%      singleton*.
%
%      H = ARAYUZ returns the handle to a new ARAYUZ or the handle to
%      the existing singleton*.
%
%      ARAYUZ('Property','Value',...) creates a new ARAYUZ using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to Arayuz_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      ARAYUZ('CALLBACK') and ARAYUZ('CALLBACK',hObject,...) call the
%      local function named CALLBACK in ARAYUZ.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Arayuz

% Last Modified by GUIDE v2.5 26-Dec-2020 22:30:19

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @Arayuz_OpeningFcn, ...
    'gui_OutputFcn',  @Arayuz_OutputFcn, ...
    'gui_LayoutFcn',  [], ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before Arayuz is made visible.
function Arayuz_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for Arayuz
t = timer('TimerFcn',{@(~,~)datetimer(handles)},'Period',1,'ExecutionMode','fixedRate');
start(t);
axes(handles.axes1);
imshow('LARESLOGO.jpg');
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Arayuz wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Arayuz_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in checkbox1.
function checkbox1_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox1


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
[files,path]=uigetfile( ...
    {'*.rad;*.rd3;*.cor',...
    'MALA Files (*.rad,*.rd3,*.cor)';...
    '*.*',  'All Files (*.*)'}, ...
    'Dosyalarý Seçiniz','MultiSelect', 'on');
if length(path)~=1 & length(files)>=1
     handles.ff = waitbar(0,'Dönüþtürmeye Baþlanýyor.');
    dinfo=dir(path);
    f1=dinfo(ismember({dinfo.name},{'Output'}));
    [m,n]=size(f1);
    if m==0
        mkdir([path,'Output']);
    end
    fidlog=fopen([path,'Output',filesep,'Ýþlem Özeti.log'],'w+');
    for i = 1:length(files)
        ff=split(files{i},'.rd3');
        if length(ff)==2
            fname=ff{1};
            filenamer=[path,fname];
            filenameo=[path,'Output',filesep,fname];
            try
                rad_hd=read_rad(filenamer);
                fprintf(fidlog,'%s.rad dosyasý baþarý ile okunmuþtur.\n',filenamer);
            catch
                fprintf(fidlog,'%s.rad dosyasý okunamamýþtýr. Dosya olmayabilir veya içeriði bozuk olabilir.\n',filenamer);
            end
            try
                [A,~]=loadrd3(filenamer);
                fprintf(fidlog,'%s.rd3 dosyasý baþarý ile okunmuþtur.\n',filenamer);
            catch
                fprintf(fidlog,'%s.rd3 dosyasý okunamamýþtýr. Dosya olmayabilir veya içeriði bozuk olabilir.\n',filenamer);
            end
            try
                head_conv=rad2head(rad_hd);
                fprintf(fidlog,'%s dosyasýnýn baþlýk dönüþümü yapýlmýþtýr.\n',filenamer);
            catch
                fprintf(fidlog,'%s dosyasýnýn baþlýk dönüþümü yapýlamamýþtýr.\n',filenamer);
            end
            if handles.checkbox1.Value==1
                cor2gps(filenamer,filenameo,fidlog);
            end
            try
                write_dt1(filenameo,head_conv,A);
                fprintf(fidlog,'%s.DT1 dosyasý baþarý ile oluþturulmuþtur.\n',filenameo);
            catch
                fprintf(fidlog,'%s.DT1 dosyasý oluþturulamamýþtýr.\n',filenameo);
            end
            try
                creatHD(filenameo,rad_hd);
                fprintf(fidlog,'%s.HD dosyasý baþarý ile oluþturulmuþtur.\n',filenameo);
            catch
                fprintf(fidlog,'%s.HD dosyasý oluþturulamamýþtýr.\n',filenameo);
            end
            fprintf(fidlog,'---------------------------------------------------\n');
            basicwaitbar(i/length(files),handles);
        end
    end
    basicwaitbar(1,handles);
    fclose all;
    close(handles.ff)
    winopen([path,'Output']);
end
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

function datetimer(handles)
text=datestr(now,'dd/mm/yyyy - HH:MM:ss');
set(handles.datetime,'String',text);


function basicwaitbar(yuzde,handles)
if yuzde==1
    waitbar(0.99,handles.ff,'Dönüþtürme Tamamlandý.');
    pause(1)
else
    waitbar(yuzde,handles.ff,'Dönüþtürme Yapýlýyor...');
end



% --- Executes during object creation, after setting all properties.
function text1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to text1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
