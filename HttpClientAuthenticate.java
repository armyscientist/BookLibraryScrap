import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.*;
//import org.json.JSONArray;

public class HttpClientAuthenticate {

    
    public static void main(String[] args) throws IOException{
        String urlParameters  = "email=example@hnlibrary.com&password=helloworld";
            byte[] postData       = urlParameters.getBytes();
            int    postDataLength = postData.length;
            String request        = "http://127.0.0.1:5000/auth";
            URL    url            = new URL( request );
            HttpURLConnection conn=null;
        try {
            //Get and prepare specifications of connection to server
            conn= (HttpURLConnection) url.openConnection();           
            conn.setDoOutput( true );
            conn.setInstanceFollowRedirects( false );
            conn.setRequestMethod( "POST" );
            
            //conn.setRequestProperty( "Content-Type", "application/x-www-form-urlencoded"); 
            conn.setRequestProperty( "charset", "utf-8");
            conn.setRequestProperty( "Content-Length", Integer.toString( postDataLength ));
            conn.setUseCaches( false );
            
            //Sending Data
            DataOutputStream wr = new DataOutputStream( conn.getOutputStream());
            wr.write( postData );

            
            String line="";                        
            InputStreamReader inputStreamReader=new InputStreamReader(conn.getInputStream()); //Get Response from server
            BufferedReader bufferedReader=new BufferedReader(inputStreamReader);
            StringBuilder response=new StringBuilder();             
            
            while ((line=bufferedReader.readLine())!=null){
                response.append(line); //storing in variable 'response'
            }
            bufferedReader.close();
            //Printing Response
            System.out.println("Response :"+response.toString());
            
            }
            catch (Exception e){
                e.printStackTrace();
                System.out.println("Error in Making POST Request");
            }
            finally{
            System.out.println("Response Code "+ conn.getResponseCode());
            }
        }
        

    } 
   /*         
            String post_data="email=value1&password=value2";

            URL url = new URL("http://127.0.0.1:5000/helloworld");
            HttpURLConnection httpURLConnection=(HttpURLConnection)url.openConnection();
            httpURLConnection.setRequestMethod("POST");
            //adding header
            httpURLConnection.setRequestProperty("Email","Password");
            //httpURLConnection.setRequestProperty("Data1","Value1");
            httpURLConnection.setDoOutput(true);

            //Adding Post Data
            OutputStream outputStream=httpURLConnection.getOutputStream();
            outputStream.write(post_data.getBytes());
            outputStream.flush();
            outputStream.close();



            System.out.println("Response Code "+httpURLConnection.getResponseCode());

            String line="";
            InputStreamReader inputStreamReader=new InputStreamReader(httpURLConnection.getInputStream());
            BufferedReader bufferedReader=new BufferedReader(inputStreamReader);
            StringBuilder response=new StringBuilder();
            while ((line=bufferedReader.readLine())!=null){
                response.append(line);
            }
            bufferedReader.close();
            System.out.println("Response : "+response.toString());



        }
        
    }


    public static void ParseJsonResponse(){
        try {
            URL url = new URL("https://jsonplaceholder.typicode.com/photos");
            HttpURLConnection httpURLConnection=(HttpURLConnection)url.openConnection();
            httpURLConnection.setRequestMethod("POST");
            
            //adding header

            String line="";
            InputStreamReader inputStreamReader=new InputStreamReader(httpURLConnection.getInputStream());
            BufferedReader bufferedReader=new BufferedReader(inputStreamReader);
            StringBuilder response=new StringBuilder();
            while ((line=bufferedReader.readLine())!=null){
                response.append(line);
            }
            bufferedReader.close();
            System.out.println("Response : "+response.toString());
            JSONArray jsonArray=new JSONArray(response.toString());
            for (int i=0;i<jsonArray.length();i++){
                System.out.println("Title : "+jsonArray.getJSONObject(i).getString("title"));
                System.out.println("ID : "+jsonArray.getJSONObject(i).getInt("id"));
                System.out.println("URL : "+jsonArray.getJSONObject(i).getString("url"));
                System.out.println("===========================================================\n");
            }

        }
        catch (Exception e){
            System.out.println("Error in Making Get Request");
        }
    }


*/

        
